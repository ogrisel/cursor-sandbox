"""Compare k-means across datasets, blob structure, and implementations.

The driver generates one float32 matrix per case and runs each
implementation in its own interpreter, so RSS high-water marks do not
leak between libraries. A worker prints one JSON object.

Phases, all with the same iteration budget (``max_iter`` or the scaled
tolerance, whichever comes first):

- ``init``: k-means++ only, then mean squared distance to the nearest center
- ``lloyd``: one Lloyd iteration from the first ``k`` rows
- ``fit``: k-means++ plus Lloyd until that budget is spent

cuML does not expose k-means++ on its own. Its init duration is a
``max_iter=1`` fit minus a one-iteration fit from fixed centers, and its
init memory is the ``max_iter=1`` fit.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
MAX_ITER = 12
TOL = 1e-8
HOME = Path.home()

CASES = [
    # Blob-iness at a fixed shape. separation / std is the cluster gap.
    dict(name="tight", kind="blobs", n=20000, d=32, k=8, separation=8.0, std=0.4, seed=10),
    dict(name="mild", kind="blobs", n=20000, d=32, k=8, separation=5.0, std=1.0, seed=11),
    dict(name="loose", kind="blobs", n=20000, d=32, k=8, separation=2.5, std=1.3, seed=12),
    dict(name="overlap", kind="blobs", n=20000, d=32, k=8, separation=1.0, std=1.6, seed=13),
    dict(name="noise", kind="normal", n=20000, d=32, k=8, seed=14),
    # Same two extremes with more features, where distances concentrate.
    dict(name="tight-d128", kind="blobs", n=20000, d=128, k=8, separation=8.0, std=0.4, seed=15),
    dict(name="noise-d128", kind="normal", n=20000, d=128, k=8, seed=16),
    # Centroid counts at the mild gap.
    dict(name="k4", kind="blobs", n=20000, d=32, k=4, separation=5.0, std=1.0, seed=20),
    dict(name="k16", kind="blobs", n=20000, d=32, k=16, separation=5.0, std=1.0, seed=21),
    dict(name="k64", kind="blobs", n=20000, d=32, k=64, separation=5.0, std=1.0, seed=22),
    dict(name="k128", kind="blobs", n=20000, d=32, k=128, separation=5.0, std=1.0, seed=23),
    # Larger matrices, still modest enough for 4 CPU cores.
    dict(name="tall", kind="blobs", n=100000, d=16, k=8, separation=5.0, std=1.0, seed=30),
    dict(name="wide", kind="blobs", n=40000, d=256, k=16, separation=5.0, std=1.0, seed=31),
    dict(name="mixed", kind="blobs", n=80000, d=64, k=32, separation=5.0, std=1.0, seed=32),
    # Shapes where a fit lasts long enough to compare throughput.
    dict(name="speed-m", kind="blobs", n=65536, d=512, k=64, separation=5.0, std=1.0, seed=40),
    dict(name="speed-l", kind="blobs", n=131072, d=1024, k=128, separation=5.0, std=1.0, seed=41),
    dict(name="speed-xl", kind="blobs", n=131072, d=2048, k=256, separation=5.0, std=1.0, seed=42),
]

IMPLS = ("torch-cpu", "sklearn-vanilla", "sklearn-optimized", "torch-cuda", "cuml")


def _pythons():
    pixi = HOME / "kmeans_lloyd/.pixi/envs/default/bin/python"
    return {
        "torch-cpu": pixi,
        "torch-cuda": pixi,
        "sklearn-vanilla": HOME / "sklearn-vanilla-venv/bin/python",
        "sklearn-optimized": HOME / "sklearn-plusplus-venv/bin/python",
        "cuml": HOME / "cuml-venv/bin/python",
    }


def generate(case, path: Path):
    rng = np.random.default_rng(case["seed"])
    n, d, k = case["n"], case["d"], case["k"]
    if case["kind"] == "normal":
        data = rng.standard_normal((n, d)).astype(np.float32)
    else:
        centers = rng.standard_normal((k, d)).astype(np.float32) * np.float32(case["separation"])
        labels = rng.integers(0, k, size=n)
        noise = rng.standard_normal((n, d)).astype(np.float32) * np.float32(case["std"])
        data = np.ascontiguousarray(centers[labels] + noise)
    path.parent.mkdir(parents=True, exist_ok=True)
    np.save(path, data)
    np.save(path.with_name(path.stem + "-centers.npy"), np.ascontiguousarray(data[:k].copy()))


def _hwm_bytes():
    for line in open("/proc/self/status"):
        if line.startswith("VmHWM:"):
            return int(line.split()[1]) * 1024
    return 0


def _mean_inertia(samples, centers, labels=None):
    centers = np.ascontiguousarray(centers, dtype=np.float32)
    if labels is not None:
        diff = samples - centers[np.asarray(labels)]
        return float(np.mean(np.sum(diff * diff, axis=1)))
    total = 0.0
    norms = np.sum(centers * centers, axis=1)
    for start in range(0, samples.shape[0], 8192):
        block = samples[start : start + 8192]
        scores = np.sum(block * block, axis=1)[:, None] + norms - 2.0 * block @ centers.T
        total += float(np.min(scores, axis=1).sum())
    return float(total / samples.shape[0])


def _tiles(n, k, cuda):
    # One Gram tile when the distance matrix is modest. The update one-hot
    # stays at 4096 rows on the GPU, where that was the faster schedule.
    tile_n = n if n * k * 4 <= 64 * 1024 * 1024 else 65536
    tile_k = k if k <= 256 else 256
    update_n = min(4096, n) if cuda else min(tile_n, n)
    return int(tile_n), int(tile_k), int(update_n)


def _time_pair(fn):
    """First call sets the RSS high water; the second call is the duration."""
    before = _hwm_bytes()
    started = time.perf_counter()
    first = fn()
    first_seconds = time.perf_counter() - started
    after = _hwm_bytes()
    started = time.perf_counter()
    second = fn()
    second_seconds = time.perf_counter() - started
    return first, second, second_seconds, max(0, after - before), first_seconds


def _worker_torch(args, samples, centers0):
    import torch

    torch.set_num_threads(4)
    cuda = args.impl == "torch-cuda"
    if cuda:
        torch.backends.cuda.matmul.allow_tf32 = False
        torch.backends.cudnn.allow_tf32 = False
        try:
            torch.set_float32_matmul_precision("highest")
        except Exception:
            pass
        data = torch.as_tensor(samples, device="cuda")
        fixed = torch.as_tensor(centers0, device="cuda")
    else:
        data = torch.as_tensor(samples)
        fixed = torch.as_tensor(centers0)
    from kmeans_lloyd.instrument import measure_call
    from kmeans_lloyd.iteration import fit_kmeans, kmeans_plusplus, lloyd_step

    tile_n, tile_k, update_n = _tiles(samples.shape[0], args.k, cuda)

    def init():
        return kmeans_plusplus(data, args.k, np.random.default_rng(args.seed))

    def lloyd():
        return lloyd_step(
            data, fixed, tile_n, tile_k, update_tile_k=min(args.k, 256), update_tile_n=update_n
        )

    def fit():
        return fit_kmeans(
            data,
            args.k,
            np.random.default_rng(args.seed),
            max_iter=args.max_iter,
            tol=args.tol,
            tile_n=tile_n,
            tile_k=tile_k,
            update_tile_k=min(args.k, 256),
            update_tile_n=update_n,
        )

    calls = {"init": init, "lloyd": lloyd, "fit": fit}
    fn = calls[args.phase]
    if cuda:
        # Warm the allocator, then measure a steady call.
        fn()
        torch.cuda.synchronize()
        result, profile = measure_call(fn, (), data)
        mem = int(profile["peak_extra_bytes"])
        seconds = float(profile["seconds"])
        meter = "torch-allocated"
    else:
        result, _, seconds, mem, _ = _time_pair(fn)
        meter = "vmhwm"
    payload = {"seconds": seconds, "mem_increment_bytes": mem, "mem_meter": meter}
    if args.phase == "init":
        centers = result[0].detach().cpu().numpy()
        payload["inertia_per_point"] = _mean_inertia(samples, centers)
    elif args.phase == "fit":
        payload["n_iter"] = int(result["n_iter"])
        payload["shift"] = float(result["shift"])
        payload["threshold"] = float(result["threshold"])
        payload["inertia_per_point"] = _mean_inertia(
            samples, result["centers"].detach().cpu().numpy(), result["labels"].detach().cpu().numpy()
        )
    else:
        payload["n_iter"] = 1
    return payload


def _worker_sklearn(args, samples, centers0):
    import sklearn
    from sklearn.cluster import KMeans, kmeans_plusplus

    def init():
        return kmeans_plusplus(samples, n_clusters=args.k, random_state=args.seed)

    def lloyd():
        model = KMeans(
            n_clusters=args.k,
            init=centers0,
            n_init=1,
            max_iter=1,
            tol=args.tol,
            algorithm="lloyd",
            random_state=args.seed,
        )
        model.fit(samples)
        return model

    def fit():
        model = KMeans(
            n_clusters=args.k,
            init="k-means++",
            n_init=1,
            max_iter=args.max_iter,
            tol=args.tol,
            algorithm="lloyd",
            random_state=args.seed,
        )
        model.fit(samples)
        return model

    fn = {"init": init, "lloyd": lloyd, "fit": fit}[args.phase]
    result, _, seconds, mem, _ = _time_pair(fn)
    payload = {
        "seconds": seconds,
        "mem_increment_bytes": mem,
        "mem_meter": "vmhwm",
        "sklearn": sklearn.__version__,
    }
    if args.phase == "init":
        payload["inertia_per_point"] = _mean_inertia(samples, np.asarray(result[0], dtype=np.float32))
        payload["center_dtype"] = str(np.asarray(result[0]).dtype)
    elif args.phase == "fit":
        labels = np.asarray(result.labels_)
        centers = np.asarray(result.cluster_centers_, dtype=np.float32)
        payload["n_iter"] = int(result.n_iter_)
        payload["inertia_per_point"] = _mean_inertia(samples, centers, labels)
        payload["center_dtype"] = str(result.cluster_centers_.dtype)
    else:
        payload["n_iter"] = int(result.n_iter_)
        payload["center_dtype"] = str(result.cluster_centers_.dtype)
    return payload


def _nvidia_used():
    text = subprocess.check_output(
        ["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"],
        text=True,
    )
    return int(text.strip().splitlines()[0]) * 1024 * 1024


def _sample_gpu(fn):
    import threading

    peak = {"value": _nvidia_used()}
    stop = {"flag": False}

    def watch():
        while not stop["flag"]:
            peak["value"] = max(peak["value"], _nvidia_used())
            time.sleep(0.02)

    thread = threading.Thread(target=watch)
    thread.start()
    started = time.perf_counter()
    try:
        result = fn()
    finally:
        stop["flag"] = True
        thread.join()
    return result, time.perf_counter() - started, peak["value"]


def _worker_cuml(args, samples, centers0):
    import cuml
    from cuml.cluster import KMeans

    def one(init, max_iter):
        model = KMeans(
            n_clusters=args.k,
            init=init,
            n_init=1,
            max_iter=max_iter,
            tol=args.tol,
            random_state=args.seed,
            output_type="numpy",
        )
        model.fit(samples)
        return model

    def lloyd():
        return one(centers0, 1)

    def fit():
        return one("k-means++", args.max_iter)

    def fit_one():
        return one("k-means++", 0)

    if args.phase == "init":
        # max_iter=0 leaves the k-means++ centers in place. fit still assigns
        # labels afterwards, so the duration includes that one assignment.
        fit_one()
        before = _nvidia_used()
        model, seconds, peak = _sample_gpu(fit_one)
        payload = {
            "seconds": seconds,
            "mem_increment_bytes": max(0, peak - before),
            "mem_meter": "nvidia-smi",
            "n_iter": int(model.n_iter_),
            "inertia_per_point": _mean_inertia(
                samples, np.asarray(model.cluster_centers_, dtype=np.float32), np.asarray(model.labels_)
            ),
            "cuml": cuml.__version__,
            "note": "max_iter=0; duration includes the assignment cuML runs after init",
        }
    elif args.phase == "lloyd":
        lloyd()
        before = _nvidia_used()
        model, seconds, peak = _sample_gpu(lloyd)
        payload = {
            "seconds": seconds,
            "mem_increment_bytes": max(0, peak - before),
            "mem_meter": "nvidia-smi",
            "n_iter": int(model.n_iter_),
            "cuml": cuml.__version__,
        }
    elif args.phase == "fit":
        fit()
        before = _nvidia_used()
        model, seconds, peak = _sample_gpu(fit)
        payload = {
            "seconds": seconds,
            "mem_increment_bytes": max(0, peak - before),
            "mem_meter": "nvidia-smi",
            "n_iter": int(model.n_iter_),
            "inertia_per_point": _mean_inertia(
                samples, np.asarray(model.cluster_centers_, dtype=np.float32), np.asarray(model.labels_)
            ),
            "cuml": cuml.__version__,
        }
    payload["mem_peak_bytes"] = peak
    payload["mem_before_bytes"] = before
    return payload


def worker(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--impl", required=True)
    parser.add_argument("--phase", required=True, choices=("init", "lloyd", "fit"))
    parser.add_argument("--data", required=True)
    parser.add_argument("--centers", required=True)
    parser.add_argument("--k", type=int, required=True)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--max-iter", type=int, default=MAX_ITER)
    parser.add_argument("--tol", type=float, default=TOL)
    args = parser.parse_args(argv)
    samples = np.load(args.data)
    centers0 = np.load(args.centers)
    os.environ.setdefault("OMP_NUM_THREADS", "4")
    os.environ.setdefault("MKL_NUM_THREADS", "4")
    os.environ.setdefault("OPENBLAS_NUM_THREADS", "4")
    if args.impl.startswith("torch"):
        payload = _worker_torch(args, samples, centers0)
    elif args.impl.startswith("sklearn"):
        payload = _worker_sklearn(args, samples, centers0)
    elif args.impl == "cuml":
        payload = _worker_cuml(args, samples, centers0)
    else:
        raise SystemExit(f"unknown impl {args.impl}")
    payload.update({"impl": args.impl, "phase": args.phase, "k": args.k})
    print(json.dumps(payload), flush=True)


def drive(selected_cases, selected_impls, out_path: Path):
    pythons = _pythons()
    data_dir = HOME / "breadth-data"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT / "src")
    env["NVIDIA_TF32_OVERRIDE"] = "0"
    env["OMP_NUM_THREADS"] = "4"
    env["MKL_NUM_THREADS"] = "4"
    env["OPENBLAS_NUM_THREADS"] = "4"
    for case in CASES:
        if selected_cases and case["name"] not in selected_cases:
            continue
        data_path = data_dir / f"{case['name']}.npy"
        generate(case, data_path)
        centers_path = data_path.with_name(data_path.stem + "-centers.npy")
        for impl in IMPLS:
            if selected_impls and impl not in selected_impls:
                continue
            for phase in ("init", "lloyd", "fit"):
                command = [
                    str(pythons[impl]),
                    str(Path(__file__).resolve()),
                    "--worker",
                    "--impl",
                    impl,
                    "--phase",
                    phase,
                    "--data",
                    str(data_path),
                    "--centers",
                    str(centers_path),
                    "--k",
                    str(case["k"]),
                    "--seed",
                    "0",
                    "--max-iter",
                    str(MAX_ITER),
                    "--tol",
                    str(TOL),
                ]
                print(f"start {case['name']} {impl} {phase}", flush=True)
                started = time.perf_counter()
                try:
                    completed = subprocess.run(
                        command,
                        cwd=str(ROOT),
                        env=env,
                        check=False,
                        capture_output=True,
                        text=True,
                        timeout=600,
                    )
                except subprocess.TimeoutExpired as exc:
                    row = {
                        "case": case,
                        "impl": impl,
                        "phase": phase,
                        "error": "timeout",
                        "stderr": (exc.stderr or "")[-2000:],
                    }
                    _append(out_path, row)
                    print("timeout", flush=True)
                    continue
                wall = time.perf_counter() - started
                line = (completed.stdout or "").strip().splitlines()
                if completed.returncode != 0 or not line:
                    row = {
                        "case": case,
                        "impl": impl,
                        "phase": phase,
                        "error": f"exit {completed.returncode}",
                        "stderr": (completed.stderr or "")[-2000:],
                        "stdout": (completed.stdout or "")[-500:],
                    }
                    _append(out_path, row)
                    print("fail", completed.returncode, flush=True)
                    continue
                payload = json.loads(line[-1])
                payload["case"] = case
                payload["wall_seconds"] = wall
                _append(out_path, payload)
                print(
                    f"  {payload.get('seconds')} mem={payload.get('mem_increment_bytes')} "
                    f"inertia={payload.get('inertia_per_point')} n_iter={payload.get('n_iter')}",
                    flush=True,
                )


def _append(path: Path, row):
    with path.open("a") as handle:
        handle.write(json.dumps(row) + "\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--cases", default="")
    parser.add_argument("--impls", default="")
    parser.add_argument("--out", default=str(HOME / "breadth-results.jsonl"))
    args, rest = parser.parse_known_args()
    if args.worker:
        worker(sys.argv[1:])
        return
    selected_cases = {name for name in args.cases.split(",") if name}
    selected_impls = {name for name in args.impls.split(",") if name}
    drive(selected_cases, selected_impls, Path(args.out))


if __name__ == "__main__":
    main()
