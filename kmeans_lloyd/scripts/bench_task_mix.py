"""Benchmark a bounded mix of KMeans tasks.

The driver stores one dataset and one set of random-row initial centers per
task/seed. Every implementation in the ``random`` track receives those exact
centers. Workers are fresh processes and have a hard 60 second wall timeout.

Array-API contenders fit ``kmeans_lloyd.KMeans``. The ``-generic`` variants
disable the PyTorch and CuPy scatter-add update so the portable one-hot
fallback is measured on the same arrays.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import threading
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
HOME = Path.home()
MAX_ITER = 12
TOL = 1e-8
TIMEOUT = 60
SEEDS = (0, 1, 2)

# Inverse pairing spans both requested logarithmic ranges without making the
# product k * d too large at both ends. ``n`` is calibrated separately.
TASKS = [
    dict(name="k3-d1000", n=950_000, d=1000, k=3, seed=101),
    dict(name="k17-d180", n=2_100_000, d=180, k=17, seed=102),
    # Keep n * k * d near the existing bounded tasks while exercising a case
    # where both the centroid count and feature width are substantial. The
    # 150k rows are calibrated to leave stock scikit-learn below 60 seconds.
    dict(name="k256-d128", n=150_000, d=128, k=256, seed=106),
    dict(name="k100-d32", n=1_500_000, d=32, k=100, seed=103),
    dict(name="k550-d6", n=525_000, d=6, k=550, seed=104),
    dict(
        name="k3000-d2",
        n=135_000,
        d=2,
        k=3000,
        seed=105,
        kind="blobs",
        true_k=300,
        separation=4,
        std=1,
        quantize=0.05,
    ),
]

API_IMPLS = (
    "torch-cpu",
    "torch-cpu-generic",
    "torch-cuda",
    "torch-cuda-generic",
    "torch-xpu",
    "torch-xpu-generic",
    "dpnp",
    "cupy",
    "cupy-generic",
)
OTHER_IMPLS = ("sklearn-vanilla", "sklearn-optimized", "cuml")
IMPLS = API_IMPLS + OTHER_IMPLS
# Initializer-only contenders. cuML's default ``scalable-k-means++`` stays
# as a reference; the array-API estimator offers only greedy k-means++.
INIT_JOBS = (
    ("torch-cpu", "plusplus"),
    ("torch-cuda", "plusplus"),
    ("torch-xpu", "plusplus"),
    ("cupy", "plusplus"),
    ("sklearn-vanilla", "plusplus"),
    ("sklearn-optimized", "plusplus"),
    ("cuml-plusplus", "plusplus"),
    ("cuml-scalable", "scalable"),
    ("cuml-random", "random"),
)


def _pythons():
    pixi = ROOT / ".pixi/envs/default/bin/python"
    default_python = Path(os.environ.get("KMEANS_PYTHON", str(pixi)))
    xpu_override = os.environ.get("KMEANS_XPU_PYTHON")
    if xpu_override:
        xpu = Path(xpu_override)
    else:
        candidate = HOME / "venvs/kmeans-lloyd-xpu/bin/python"
        xpu = candidate if candidate.exists() else default_python
    sklearn = Path(
        os.environ.get(
            "KMEANS_SKLEARN_PYTHON",
            str(HOME / "sklearn-vanilla-venv/bin/python"),
        )
    )
    pythons = {name: default_python for name in API_IMPLS}
    pythons["torch-xpu"] = xpu
    pythons["torch-xpu-generic"] = xpu
    pythons["dpnp"] = xpu
    pythons.update(
        {
            "random-baseline": pixi,
            "sklearn-vanilla": sklearn,
            "sklearn-optimized": Path(
                os.environ.get(
                    "KMEANS_SKLEARN_OPTIMIZED_PYTHON",
                    str(HOME / "sklearn-plusplus-venv/bin/python"),
                )
            ),
            "cuml": HOME / "cuml-venv/bin/python",
            "cuml-plusplus": HOME / "cuml-venv/bin/python",
            "cuml-scalable": HOME / "cuml-venv/bin/python",
            "cuml-random": HOME / "cuml-venv/bin/python",
        }
    )
    return pythons


def generate(task, path):
    """Generate float32 Gaussian-noise tasks directly into an npy memmap."""
    if path.exists():
        shape = np.load(path, mmap_mode="r").shape
        if shape == (task["n"], task["d"]):
            return
        path.unlink()
    path.parent.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(task["seed"])
    truth = None
    if task.get("kind") == "blobs":
        truth = (
            rng.standard_normal((task["true_k"], task["d"])).astype(np.float32)
            * np.float32(task["separation"])
        )
    data = np.lib.format.open_memmap(path, mode="w+", dtype=np.float32, shape=(task["n"], task["d"]))
    for start in range(0, task["n"], 8192):
        stop = min(start + 8192, task["n"])
        noise = rng.standard_normal((stop - start, task["d"])).astype(np.float32)
        if truth is None:
            data[start:stop] = noise
        else:
            labels = rng.integers(0, task["true_k"], size=stop - start)
            data[start:stop] = truth[labels] + np.float32(task["std"]) * noise
        if task.get("quantize"):
            quantum = np.float32(task["quantize"])
            data[start:stop] = np.round(data[start:stop] / quantum) * quantum
    del data


def save_random_start(data_path, task, seed):
    rng = np.random.default_rng(seed)
    indices = rng.choice(task["n"], size=task["k"], replace=False)
    data = np.load(data_path, mmap_mode="r")
    stem = data_path.with_name(data_path.stem + f"-seed-{seed}")
    np.save(stem.with_name(stem.name + "-indices.npy"), indices)
    np.save(stem.with_name(stem.name + "-centers.npy"), np.ascontiguousarray(data[indices]))
    return (
        stem.with_name(stem.name + "-indices.npy"),
        stem.with_name(stem.name + "-centers.npy"),
    )


def _hwm_bytes():
    for line in Path("/proc/self/status").read_text().splitlines():
        if line.startswith("VmHWM:"):
            return int(line.split()[1]) * 1024
    return 0


def _mean_inertia(samples, centers):
    centers = np.ascontiguousarray(centers, dtype=np.float32)
    block_n = max(1, min(8192, (64 * 1024 * 1024) // (4 * len(centers))))
    norms = np.sum(centers * centers, axis=1)
    total = 0.0
    for start in range(0, len(samples), block_n):
        block = samples[start : start + block_n]
        scores = np.sum(block * block, axis=1)[:, None] + norms - 2 * block @ centers.T
        total += float(np.min(scores, axis=1).sum())
    return total / len(samples)


def _to_numpy(array):
    module = type(array).__module__
    if module.startswith("torch"):
        return array.detach().cpu().numpy()
    if module.startswith("cupy"):
        return array.get()
    if module.startswith("dpnp"):
        import dpnp

        return dpnp.asnumpy(array)
    return np.asarray(array)


def _torch_target(impl):
    """Return ``cpu``, ``cuda``, or ``xpu`` for a PyTorch contender name."""
    if "xpu" in impl:
        return "xpu"
    if "cpu" in impl:
        return "cpu"
    return "cuda"


def _sync_dpnp(result):
    """Wait for the queue that owns the fitted centers or initializer output."""
    array = result.cluster_centers_ if hasattr(result, "cluster_centers_") else result[0]
    array.sycl_queue.wait()


def _worker_api(args, samples, centers0):
    backend = args.impl.split("-")[0]
    target = _torch_target(args.impl) if backend == "torch" else "cuda"
    gpu = backend != "dpnp" and target in ("cuda", "xpu")
    # dpnp has no hooked keyed reduction, so the portable update always runs.
    native = backend != "dpnp" and not args.impl.endswith("-generic")
    versions = {}
    if backend == "dpnp":
        import dpnp

        versions["dpnp"] = dpnp.__version__
        versions["device"] = "gpu"
        data = dpnp.asarray(samples, device="gpu")
        fixed = dpnp.asarray(centers0, device="gpu")
        versions["sycl_device"] = str(data.sycl_device)
        warm = dpnp.ones((2, 2), dtype=dpnp.float32, device="gpu")
        (warm @ warm).sycl_queue.wait()
    elif backend == "torch":
        import torch

        torch.set_num_threads(4)
        torch.set_float32_matmul_precision("highest")
        versions["torch"] = torch.__version__
        versions["device"] = target
        if target == "cuda":
            torch.backends.cuda.matmul.allow_tf32 = False
            torch.backends.cudnn.allow_tf32 = False
            data = torch.as_tensor(samples, device="cuda")
            fixed = torch.as_tensor(centers0, device="cuda")
            torch.ones((2, 2), device="cuda") @ torch.ones((2, 2), device="cuda")
            torch.cuda.synchronize()
        elif target == "xpu":
            versions["xpu_name"] = torch.xpu.get_device_name(0)
            data = torch.as_tensor(samples, device="xpu")
            fixed = torch.as_tensor(centers0, device="xpu")
            torch.ones((2, 2), device="xpu") @ torch.ones((2, 2), device="xpu")
            torch.xpu.synchronize()
        else:
            data = torch.as_tensor(samples)
            fixed = torch.as_tensor(centers0)
    else:
        import cupy

        data = cupy.asarray(samples)
        fixed = cupy.asarray(centers0)
        cupy.ones((2, 2), dtype=cupy.float32) @ cupy.ones((2, 2), dtype=cupy.float32)
        cupy.cuda.Stream.null.synchronize()

    from kmeans_lloyd import KMeans
    from kmeans_lloyd.backends import use_native_backends
    from kmeans_lloyd.instrument import measure_call
    from kmeans_lloyd.iteration import kmeans_plusplus

    use_native_backends(native)

    def call():
        if args.phase == "init":
            return kmeans_plusplus(data, args.k, np.random.default_rng(args.seed))
        model = KMeans(
            n_clusters=args.k,
            init="k-means++" if args.init == "plusplus" else fixed,
            n_init=1,
            max_iter=args.max_iter,
            tol=args.tol,
            random_state=args.seed,
        )
        return model.fit(data)

    if backend == "dpnp":
        data.sycl_queue.wait()
        before = _hwm_bytes()
        started = time.perf_counter()
        result = call()
        _sync_dpnp(result)
        seconds = time.perf_counter() - started
        memory = max(0, _hwm_bytes() - before)
        meter = "vmhwm"
    elif gpu:
        result, profile = measure_call(call, (), data)
        seconds = profile["seconds"]
        memory = profile["peak_extra_bytes"]
        meter = "xpu-pool" if target == "xpu" else f"{backend}-pool"
    else:
        before = _hwm_bytes()
        started = time.perf_counter()
        result = call()
        seconds = time.perf_counter() - started
        memory = max(0, _hwm_bytes() - before)
        meter = "vmhwm"
    payload = {
        "seconds": seconds,
        "mem_increment_bytes": memory,
        "mem_meter": meter,
        "n_iter": 0 if args.phase == "init" else int(result.n_iter_),
        "inertia_per_point": _mean_inertia(
            samples,
            _to_numpy(result[0] if args.phase == "init" else result.cluster_centers_),
        ),
        **versions,
    }
    if args.phase != "init":
        payload["native_update"] = native
    return payload


def _worker_sklearn(args, samples, centers0):
    import sklearn
    from sklearn.cluster import KMeans, kmeans_plusplus

    if args.phase == "init":
        before = _hwm_bytes()
        started = time.perf_counter()
        centers, _indices = kmeans_plusplus(
            samples, n_clusters=args.k, random_state=args.seed
        )
        seconds = time.perf_counter() - started
        memory = max(0, _hwm_bytes() - before)
        return {
            "seconds": seconds,
            "mem_increment_bytes": memory,
            "mem_meter": "vmhwm",
            "n_iter": 0,
            "inertia_per_point": _mean_inertia(samples, np.asarray(centers, dtype=np.float32)),
            "sklearn": sklearn.__version__,
        }

    model = KMeans(
        n_clusters=args.k,
        init="k-means++" if args.init == "plusplus" else centers0,
        n_init=1,
        max_iter=args.max_iter,
        tol=args.tol,
        algorithm="lloyd",
        random_state=args.seed,
    )
    before = _hwm_bytes()
    started = time.perf_counter()
    model.fit(samples)
    seconds = time.perf_counter() - started
    memory = max(0, _hwm_bytes() - before)
    return {
        "seconds": seconds,
        "mem_increment_bytes": memory,
        "mem_meter": "vmhwm",
        "n_iter": int(model.n_iter_),
        "inertia_per_point": _mean_inertia(samples, model.cluster_centers_),
        "sklearn": sklearn.__version__,
    }


def _nvidia_used():
    output = subprocess.check_output(
        ["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"],
        text=True,
    )
    return int(output.splitlines()[0]) * 1024 * 1024


def _sample_gpu(fn):
    peak = {"value": _nvidia_used()}
    stop = {"value": False}

    def watch():
        while not stop["value"]:
            peak["value"] = max(peak["value"], _nvidia_used())
            time.sleep(0.02)

    thread = threading.Thread(target=watch)
    thread.start()
    started = time.perf_counter()
    try:
        result = fn()
    finally:
        stop["value"] = True
        thread.join()
    return result, time.perf_counter() - started, peak["value"]


def _worker_cuml_init(args, samples):
    """Time one cuML initializer with ``max_iter=0``.

    That fit still assigns every sample once so it can store labels. A second
    fit from the resulting centers repeats only that assignment. The reported
    duration is the difference. Memory is the nvidia-smi rise of the
    initialization fit above data already resident on the device.
    """
    import cuml
    import cupy
    from cuml.cluster import KMeans

    data = cupy.asarray(samples)
    cupy.cuda.Stream.null.synchronize()
    warm_rows = min(int(data.shape[0]), 128)
    KMeans(
        n_clusters=min(2, args.k),
        init="random",
        n_init=1,
        max_iter=0,
        random_state=0,
        output_type="cupy",
    ).fit(data[:warm_rows])
    cupy.cuda.Stream.null.synchronize()

    init = {
        "plusplus": "k-means++",
        "scalable": "scalable-k-means++",
        "random": "random",
    }[args.init]

    def initialize():
        model = KMeans(
            n_clusters=args.k,
            init=init,
            n_init=1,
            max_iter=0,
            tol=args.tol,
            random_state=args.seed,
            oversampling_factor=args.oversampling_factor,
            output_type="cupy",
        )
        model.fit(data)
        cupy.cuda.Stream.null.synchronize()
        return model

    def assign(centers):
        model = KMeans(
            n_clusters=args.k,
            init=centers,
            n_init=1,
            max_iter=0,
            tol=args.tol,
            random_state=args.seed,
            output_type="cupy",
        )
        model.fit(data)
        cupy.cuda.Stream.null.synchronize()
        return model

    before = _nvidia_used()
    model, fit_seconds, peak = _sample_gpu(initialize)
    centers = cupy.ascontiguousarray(model.cluster_centers_, dtype=cupy.float32)
    assign_before = _nvidia_used()
    _, assign_seconds, assign_peak = _sample_gpu(lambda: assign(centers))
    return {
        "seconds": max(0.0, fit_seconds - assign_seconds),
        "fit_seconds": fit_seconds,
        "assign_seconds": assign_seconds,
        "mem_increment_bytes": max(0, peak - before),
        "assign_mem_increment_bytes": max(0, assign_peak - assign_before),
        "mem_meter": "nvidia-smi",
        "n_iter": int(model.n_iter_),
        "inertia_per_point": _mean_inertia(samples, cupy.asnumpy(centers)),
        "cuml": cuml.__version__,
    }


def _worker_cuml(args, samples, centers0):
    import cuml
    import cupy
    from cuml.cluster import KMeans

    # Match the array-API contenders: transfer the data and shared
    # random-row centers before starting the timed fit.
    data = cupy.asarray(samples)
    fixed = cupy.asarray(centers0)
    cupy.cuda.Stream.null.synchronize()

    def call():
        model = KMeans(
            n_clusters=args.k,
            init={"plusplus": "k-means++", "scalable": "scalable-k-means++"}.get(
                args.init, fixed
            ),
            n_init=1,
            max_iter=args.max_iter,
            tol=args.tol,
            random_state=args.seed,
            oversampling_factor=args.oversampling_factor,
            output_type="cupy",
        )
        model.fit(data)
        cupy.cuda.Stream.null.synchronize()
        return model

    before = _nvidia_used()
    model, seconds, peak = _sample_gpu(call)
    return {
        "seconds": seconds,
        "mem_increment_bytes": max(0, peak - before),
        "mem_meter": "nvidia-smi",
        "n_iter": int(model.n_iter_),
        "inertia_per_point": _mean_inertia(samples, cupy.asnumpy(model.cluster_centers_)),
        "cuml": cuml.__version__,
    }


def _worker_baseline(args, samples, indices):
    before = _hwm_bytes()
    started = time.perf_counter()
    centers = np.ascontiguousarray(samples[indices])
    seconds = time.perf_counter() - started
    memory = max(0, _hwm_bytes() - before)
    return {
        "seconds": seconds,
        "mem_increment_bytes": memory,
        "mem_meter": "vmhwm",
        "n_iter": 0,
        "inertia_per_point": _mean_inertia(samples, centers),
    }


def worker(argv):
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--phase", choices=("fit", "init"), default="fit")
    parser.add_argument("--impl", required=True)
    parser.add_argument("--init", choices=("plusplus", "scalable", "random"), required=True)
    parser.add_argument("--data", required=True)
    parser.add_argument("--centers", required=True)
    parser.add_argument("--indices", required=True)
    parser.add_argument("--k", type=int, required=True)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--max-iter", type=int, default=MAX_ITER)
    parser.add_argument("--tol", type=float, default=TOL)
    parser.add_argument("--oversampling-factor", type=float, default=2.0)
    parser.add_argument("--init-rounds", type=int, default=8)
    args = parser.parse_args(argv)
    samples = np.load(args.data)
    centers0 = np.load(args.centers)
    indices = np.load(args.indices)
    if args.impl.startswith(("torch", "cupy", "dpnp")):
        payload = _worker_api(args, samples, centers0)
    elif args.impl.startswith("sklearn"):
        payload = _worker_sklearn(args, samples, centers0)
    elif args.impl.startswith("cuml") and args.phase == "init":
        payload = _worker_cuml_init(args, samples)
    elif args.impl == "cuml":
        payload = _worker_cuml(args, samples, centers0)
    elif args.impl == "random-baseline":
        payload = _worker_baseline(args, samples, indices)
    else:
        raise ValueError(args.impl)
    payload.update(
        {
            "impl": args.impl,
            "init": args.init,
            "phase": args.phase,
            "seed": args.seed,
            "k": args.k,
        }
    )
    print(json.dumps(payload), flush=True)


def _append(path, row):
    with path.open("a") as stream:
        stream.write(json.dumps(row) + "\n")


def _cpu_affinity(impl):
    """Pin host contenders to ``KMEANS_CPUSET`` when that variable is set.

    XPU and CUDA workers are left unpinned so the device runtime can use the
    rest of the host. An empty variable keeps the historical unbound behavior.
    """
    cpuset = os.environ.get("KMEANS_CPUSET", "")
    if not cpuset or not impl.startswith(("torch-cpu", "sklearn", "random")):
        return []
    return ["taskset", "-c", cpuset]


def _run_worker(command, env, timeout):
    return subprocess.run(
        command,
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        timeout=timeout,
    )


def drive(
    selected_tasks,
    selected_impls,
    selected_inits,
    seeds,
    out,
    calibrate=False,
    phase="fit",
    oversampling_factor=2.0,
    init_rounds=8,
    timeout=TIMEOUT,
):
    data_dir = HOME / "task-mix-data-v4"
    env = os.environ.copy()
    env.update(
        PYTHONPATH=str(ROOT / "src"),
        NVIDIA_TF32_OVERRIDE="0",
        OMP_NUM_THREADS="4",
        MKL_NUM_THREADS="4",
        OPENBLAS_NUM_THREADS="4",
    )
    pythons = _pythons()
    for task in TASKS:
        if selected_tasks and task["name"] not in selected_tasks:
            continue
        data_path = data_dir / f"{task['name']}.npy"
        generate(task, data_path)
        for seed in seeds:
            indices_path, centers_path = save_random_start(data_path, task, seed)
            if calibrate:
                jobs = [("sklearn-vanilla", "plusplus")]
            elif phase == "init":
                jobs = list(INIT_JOBS)
                jobs.append(("random-baseline", "random"))
            else:
                jobs = [(impl, init) for impl in IMPLS for init in ("plusplus", "random")]
                jobs.append(("cuml", "scalable"))
                jobs.append(("random-baseline", "random"))
            for impl, init in jobs:
                if selected_impls and impl not in selected_impls:
                    continue
                if selected_inits and init not in selected_inits:
                    continue
                command = [
                    *_cpu_affinity(impl),
                    str(pythons[impl]),
                    str(Path(__file__).resolve()),
                    "--worker",
                    "--phase",
                    phase,
                    "--impl",
                    impl,
                    "--init",
                    init,
                    "--data",
                    str(data_path),
                    "--centers",
                    str(centers_path),
                    "--indices",
                    str(indices_path),
                    "--k",
                    str(task["k"]),
                    "--seed",
                    str(seed),
                    "--oversampling-factor",
                    str(oversampling_factor),
                    "--init-rounds",
                    str(init_rounds),
                ]
                if (
                    os.environ.get("KMEANS_WARMUP") == "1"
                    and impl.startswith(("torch-xpu", "dpnp"))
                    and seed == seeds[0]
                ):
                    print(f"warmup {task['name']} {phase} {impl} {init}", flush=True)
                    warm_started = time.perf_counter()
                    try:
                        _run_worker(command, env, max(timeout, 300))
                    except subprocess.TimeoutExpired:
                        print("  warmup timeout", flush=True)
                    else:
                        print(f"  warmup {time.perf_counter() - warm_started:.1f}s", flush=True)
                print(f"start {task['name']} seed={seed} {phase} {impl} {init}", flush=True)
                wall_started = time.perf_counter()
                try:
                    completed = _run_worker(command, env, timeout)
                except subprocess.TimeoutExpired as error:
                    row = {
                        "task": task,
                        "seed": seed,
                        "impl": impl,
                        "init": init,
                        "phase": phase,
                        "error": "timeout",
                        "timeout_seconds": timeout,
                        "stderr": (error.stderr or "")[-1000:],
                    }
                    _append(out, row)
                    print("  timeout", flush=True)
                    continue
                lines = completed.stdout.strip().splitlines()
                if completed.returncode or not lines:
                    row = {
                        "task": task,
                        "seed": seed,
                        "impl": impl,
                        "init": init,
                        "phase": phase,
                        "error": f"exit {completed.returncode}",
                        "stderr": completed.stderr[-2000:],
                    }
                    _append(out, row)
                    print(f"  exit {completed.returncode}", flush=True)
                    continue
                row = json.loads(lines[-1])
                row["task"] = task
                row["phase"] = phase
                row["wall_seconds"] = time.perf_counter() - wall_started
                _append(out, row)
                print(
                    f"  {row['seconds']:.3f}s inertia={row['inertia_per_point']:.3f} "
                    f"iter={row['n_iter']}",
                    flush=True,
                )


def main():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--tasks", default="")
    parser.add_argument("--impls", default="")
    parser.add_argument("--inits", default="")
    parser.add_argument("--seeds", default="0,1,2")
    parser.add_argument("--out", default=str(HOME / "task-mix-results.jsonl"))
    parser.add_argument("--calibrate", action="store_true")
    parser.add_argument("--phase", choices=("fit", "init"), default="fit")
    parser.add_argument("--oversampling-factor", type=float, default=2.0)
    parser.add_argument("--init-rounds", type=int, default=8)
    parser.add_argument("--timeout", type=int, default=TIMEOUT)
    args, _ = parser.parse_known_args()
    if args.worker:
        worker(sys.argv[1:])
        return
    tasks = {value for value in args.tasks.split(",") if value}
    impls = {value for value in args.impls.split(",") if value}
    inits = {value for value in args.inits.split(",") if value}
    seeds = [int(value) for value in args.seeds.split(",") if value]
    drive(
        tasks,
        impls,
        inits,
        seeds,
        Path(args.out),
        calibrate=args.calibrate,
        phase=args.phase,
        oversampling_factor=args.oversampling_factor,
        init_rounds=args.init_rounds,
        timeout=args.timeout,
    )


if __name__ == "__main__":
    main()
