"""Tile-size sweep, Lloyd step, and k-means++ on the L4.

The core routines are the array-API functions in ``kmeans_lloyd.iteration``.
``torch.compile`` is applied here, around those functions, and the same
functions are what the eager rows call.
"""

from __future__ import annotations

import argparse
import gc
import json
import os
import platform
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

os.environ.setdefault("NVIDIA_TF32_OVERRIDE", "0")

# Feature-heavy shape from the fusion journal: one GEMM assignment is about
# a second, and the distance matrix is 1 GiB rather than 4 GiB.
FEATURE = {"name": "feature-heavy", "n_samples": 65_536, "n_clusters": 4_096, "n_features": 16_384}
# Shared with the Cython benchmark. Large enough for a multi-second CPU
# Lloyd step and small enough to generate on the host.
COMPARE = {"name": "cython-compare", "n_samples": 65_536, "n_clusters": 1_024, "n_features": 2_048}
PLUSPLUS = {"name": "kmeans-plusplus", "n_samples": 65_536, "n_clusters": 1_024, "n_features": 8_192}

GEMM_TILES = (
    (256, 4096),
    (1024, 4096),
    (4096, 4096),
    (65536, 4096),
    (4096, 1024),
    (4096, 256),
    (1024, 1024),
    (1024, 256),
)
RUNNING_TILES = (16, 32, 64, 128, 256)


def _configure_torch():
    import torch

    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    try:
        torch.set_float32_matmul_precision("highest")
    except Exception:
        pass
    return torch


def _cleanup():
    gc.collect()
    import torch

    torch.cuda.synchronize()
    torch.cuda.empty_cache()
    gc.collect()


def _median(values):
    ordered = sorted(values)
    mid = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[mid]
    return 0.5 * (ordered[mid - 1] + ordered[mid])


def _bench(fn, args, example, warmup, repeats):
    from kmeans_lloyd.instrument import measure_call

    profiles = []
    output = None
    for index in range(warmup + repeats):
        output, profile = measure_call(fn, args, example)
        profile["warmup"] = index < warmup
        profiles.append(profile)
        del output
    steady = [row for row in profiles if not row["warmup"]]
    return {
        "status": "ok",
        "median_seconds": _median([row["seconds"] for row in steady]),
        "median_peak_extra_bytes": int(_median([row["peak_extra_bytes"] for row in steady])),
        "profiles": [{key: row[key] for key in ("seconds", "peak_extra_bytes", "warmup")} for row in profiles],
    }


def _compile(fn, example_args):
    import torch

    torch._dynamo.reset()
    started = time.perf_counter()
    compiled = torch.compile(fn, fullgraph=False, backend="inductor")
    try:
        out = compiled(*example_args)
        torch.cuda.synchronize()
        compile_seconds = time.perf_counter() - started
        del out
        return compiled, {"compile_seconds": compile_seconds, "error": None}
    except Exception as exc:
        _cleanup()
        torch._dynamo.reset()
        return None, {"compile_seconds": None, "error": f"{type(exc).__name__}: {exc}"}


def _kernels(fn, args):
    import torch
    from torch.profiler import ProfilerActivity, profile

    torch.cuda.synchronize()
    with profile(activities=[ProfilerActivity.CUDA]) as prof:
        fn(*args)
        torch.cuda.synchronize()
    rows = []
    for event in prof.key_averages():
        device_time = getattr(event, "device_time_total", 0) or 0
        if not device_time:
            continue
        rows.append({"name": event.key, "count": int(event.count), "device_time_us": float(device_time)})
    rows.sort(key=lambda row: row["device_time_us"], reverse=True)
    return rows[:8]


def _save(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n")
    print(f"wrote {path}", flush=True)


def _feature_inputs(torch):
    generator = torch.Generator(device="cuda")
    generator.manual_seed(0)
    samples = torch.randn(
        FEATURE["n_samples"],
        FEATURE["n_features"],
        device="cuda",
        dtype=torch.float32,
        generator=generator,
    )
    centroids = samples[: FEATURE["n_clusters"]].contiguous()
    return samples, centroids


def _host_inputs(torch, case, seed):
    import numpy as np

    rng = np.random.default_rng(seed)
    samples_np = rng.standard_normal((case["n_samples"], case["n_features"])).astype(np.float32)
    centroids_np = np.ascontiguousarray(samples_np[: case["n_clusters"]])
    samples = torch.as_tensor(samples_np, device="cuda")
    centroids = torch.as_tensor(centroids_np, device="cuda")
    return samples, centroids, samples_np, centroids_np


def _check(torch):
    from kmeans_lloyd.iteration import (
        assign_gemm_tiled,
        assign_naive,
        assign_running_stateful,
        kmeans_plusplus,
        lloyd_step,
    )

    samples = torch.randn(48, 6, device="cuda", dtype=torch.float64)
    centroids = samples[:5].contiguous()
    reference = assign_naive(samples, centroids)
    if not torch.equal(reference, assign_gemm_tiled(samples, centroids, tile_n=7, tile_k=2)):
        raise SystemExit("gemm tiles disagreed with naive assignment")
    if not torch.equal(reference, assign_running_stateful(samples, centroids, tile_k=2)):
        raise SystemExit("stateful running tiles disagreed with naive assignment")
    updated, labels = lloyd_step(samples, centroids, tile_n=7, tile_k=2)
    if labels.shape != (48,) or updated.shape != centroids.shape:
        raise SystemExit("lloyd_step returned an unexpected shape")
    centers, indices = kmeans_plusplus(samples.float(), 4, __import__("numpy").random.default_rng(1))
    if centers.shape != (4, 6) or indices.shape != (4,):
        raise SystemExit("kmeans_plusplus returned an unexpected shape")
    print("device checks passed", flush=True)


def _run_gemm_tiles(torch, samples, centroids, folder):
    from kmeans_lloyd.iteration import assign_gemm, assign_gemm_tiled, gemm_scores_argmin
    from array_api_compat import array_namespace

    rows = []
    payload = {"meta": _meta(torch), "case": FEATURE, "runs": rows}

    def gemm_tile(x_tile, c_tile, c_norm):
        return gemm_scores_argmin(array_namespace(x_tile, c_tile, c_norm), x_tile, c_tile, c_norm)

    for mode in ("eager", "compiled"):
        for tile_n, tile_k in GEMM_TILES:
            name = f"gemm-{mode}-{tile_n}x{tile_k}"
            print(f"start {name}", flush=True)
            step = None
            compile_info = None
            if mode == "compiled":
                example_x = samples[:tile_n]
                example_c = centroids[:tile_k]
                example_norm = (example_c * example_c).sum(dim=1)
                step, compile_info = _compile(gemm_tile, (example_x, example_c, example_norm))
                if step is None:
                    rows.append({"name": name, "tile_n": tile_n, "tile_k": tile_k, "mode": mode, "status": "error", "compile": compile_info})
                    _save(folder / "results.json", payload)
                    continue
            result = _bench(
                lambda x, c, step=step, tile_n=tile_n, tile_k=tile_k: assign_gemm_tiled(x, c, tile_n, tile_k, step=step),
                (samples, centroids),
                samples,
                warmup=1,
                repeats=2,
            )
            result.update({"name": name, "tile_n": tile_n, "tile_k": tile_k, "mode": mode, "compile": compile_info})
            rows.append(result)
            print(
                f"done {name} {result['median_seconds']:.4f}s peak {result['median_peak_extra_bytes']}",
                flush=True,
            )
            _cleanup()
            _save(folder / "results.json", payload)
    print("start gemm-eager-full", flush=True)
    full = _bench(assign_gemm, (samples, centroids), samples, warmup=1, repeats=2)
    full.update({"name": "gemm-eager-full", "mode": "eager"})
    rows.append(full)
    print(f"done gemm-eager-full {full['median_seconds']:.4f}s peak {full['median_peak_extra_bytes']}", flush=True)
    _cleanup()
    _save(folder / "results.json", payload)
    return payload


def _run_running(torch, samples, centroids, folder):
    from kmeans_lloyd.iteration import assign_running_stateful, assign_running_tiled, running_tile_distances, running_tile_update

    path = folder / "results.json"
    payload = json.loads(path.read_text()) if path.exists() else {"meta": _meta(torch), "case": FEATURE, "runs": []}
    rows = payload.setdefault("running", [])
    for tile_k in RUNNING_TILES:
        for kind, fn, builder in (
            (
                "tiled",
                assign_running_tiled,
                lambda tile, samples=samples, centroids=centroids: running_tile_distances(samples, centroids[:tile]),
            ),
            (
                "stateful",
                assign_running_stateful,
                lambda tile, samples=samples, centroids=centroids: running_tile_update(
                    samples,
                    centroids[:tile],
                    torch.full((samples.shape[0],), float("inf"), device="cuda"),
                    torch.zeros(samples.shape[0], dtype=torch.int64, device="cuda"),
                    torch.zeros((), dtype=torch.int64, device="cuda"),
                ),
            ),
        ):
            name = f"running-{kind}-k{tile_k}"
            print(f"start {name}", flush=True)
            if kind == "tiled":
                compiled, info = _compile(running_tile_distances, (samples, centroids[:tile_k]))
                call = lambda x, c, compiled=compiled, tile_k=tile_k: fn(x, c, tile_k, block=compiled)
            else:
                compiled, info = _compile(
                    running_tile_update,
                    (
                        samples,
                        centroids[:tile_k],
                        torch.full((samples.shape[0],), float("inf"), device="cuda"),
                        torch.zeros(samples.shape[0], dtype=torch.int64, device="cuda"),
                        torch.zeros((), dtype=torch.int64, device="cuda"),
                    ),
                )
                call = lambda x, c, compiled=compiled, tile_k=tile_k: fn(x, c, tile_k, block=compiled)
            if compiled is None:
                rows.append({"name": name, "tile_k": tile_k, "kind": kind, "status": "error", "compile": info})
                _save(path, payload)
                continue
            result = _bench(call, (samples, centroids), samples, warmup=1, repeats=1)
            result.update({"name": name, "tile_k": tile_k, "kind": kind, "compile": info})
            rows.append(result)
            print(
                f"done {name} {result['median_seconds']:.4f}s compile {info['compile_seconds']:.2f}s peak {result['median_peak_extra_bytes']}",
                flush=True,
            )
            del compiled
            _cleanup()
            _save(path, payload)
            if result["median_seconds"] > 20:
                print(f"stop running sweep after {name}", flush=True)
                return payload
    return payload


def _profile(torch, samples, centroids, folder):
    from kmeans_lloyd.iteration import assign_gemm_tiled, gemm_scores_argmin, running_tile_update
    from array_api_compat import array_namespace

    path = folder / "results.json"
    payload = json.loads(path.read_text())

    def gemm_tile(x_tile, c_tile, c_norm):
        return gemm_scores_argmin(array_namespace(x_tile, c_tile, c_norm), x_tile, c_tile, c_norm)

    compiled, info = _compile(gemm_tile, (samples[:4096], centroids[:1024], (centroids[:1024] * centroids[:1024]).sum(dim=1)))
    profiles = []
    if compiled is not None:
        profiles.append(
            {
                "name": "compiled-gemm-tile-4096x1024",
                "compile": info,
                "kernels": _kernels(compiled, (samples[:4096], centroids[:1024], (centroids[:1024] * centroids[:1024]).sum(dim=1))),
            }
        )
    compiled_running, info = _compile(
        running_tile_update,
        (
            samples,
            centroids[:32],
            torch.full((samples.shape[0],), float("inf"), device="cuda"),
            torch.zeros(samples.shape[0], dtype=torch.int64, device="cuda"),
            torch.zeros((), dtype=torch.int64, device="cuda"),
        ),
    )
    if compiled_running is not None:
        profiles.append(
            {
                "name": "compiled-running-stateful-k32",
                "compile": info,
                "kernels": _kernels(
                    compiled_running,
                    (
                        samples,
                        centroids[:32],
                        torch.full((samples.shape[0],), float("inf"), device="cuda"),
                        torch.zeros(samples.shape[0], dtype=torch.int64, device="cuda"),
                        torch.zeros((), dtype=torch.int64, device="cuda"),
                    ),
                ),
            }
        )
    payload["profiles"] = profiles
    _save(path, payload)
    _ = assign_gemm_tiled  # kept imported so a profile edit can call the full assign
    return payload


def _lloyd(torch, folder):
    from kmeans_lloyd.instrument import PhaseRecorder
    from kmeans_lloyd.iteration import assign_gemm, lloyd_iteration, lloyd_step, update_centroids, update_centroids_tiled

    path = folder / "results.json"
    payload = json.loads(path.read_text()) if path.exists() else {"meta": _meta(torch), "runs": []}
    samples, centroids = _feature_inputs(torch)
    runs = payload.setdefault("lloyd", [])
    specs = [
        ("gemm-one-hot", lambda: lloyd_iteration(samples, centroids, assign="gemm", recorder=PhaseRecorder(samples))),
        ("tiled-4096x1024", lambda: lloyd_step(samples, centroids, 4096, 1024, update_tile_k=256, recorder=PhaseRecorder(samples))),
        ("tiled-256x4096", lambda: lloyd_step(samples, centroids, 256, 4096, update_tile_k=256, recorder=PhaseRecorder(samples))),
    ]
    for name, call in specs:
        print(f"start lloyd {name}", flush=True)
        recorder_box = {}

        def wrapped(name=name, call=call):
            updated, labels = call()
            return updated, labels

        # Rebuild with a recorder we can read. The lambdas above each construct one.
        if name == "gemm-one-hot":
            recorder = PhaseRecorder(samples)
            fn = lambda samples=samples, centroids=centroids, recorder=recorder: lloyd_iteration(
                samples, centroids, assign="gemm", recorder=recorder
            )
        elif name == "tiled-4096x1024":
            recorder = PhaseRecorder(samples)
            fn = lambda samples=samples, centroids=centroids, recorder=recorder: lloyd_step(
                samples, centroids, 4096, 1024, update_tile_k=256, recorder=recorder
            )
        else:
            recorder = PhaseRecorder(samples)
            fn = lambda samples=samples, centroids=centroids, recorder=recorder: lloyd_step(
                samples, centroids, 256, 4096, update_tile_k=256, recorder=recorder
            )
        _ = (assign_gemm, update_centroids, update_centroids_tiled, wrapped, recorder_box)
        result = _bench(fn, (), samples, warmup=1, repeats=1)
        result.update({"name": name, "phases": recorder.phases})
        runs.append(result)
        print(f"done lloyd {name} {result['median_seconds']:.4f}s phases {recorder.phases}", flush=True)
        _cleanup()
        _save(path, payload)
    compare_samples, compare_centroids, samples_np, centroids_np = _host_inputs(torch, COMPARE, seed=0)
    recorder = PhaseRecorder(compare_samples)
    result = _bench(
        lambda: lloyd_step(compare_samples, compare_centroids, 256, COMPARE["n_clusters"], update_tile_k=256, recorder=recorder),
        (),
        compare_samples,
        warmup=1,
        repeats=2,
    )
    labels = lloyd_step(compare_samples, compare_centroids, 256, COMPARE["n_clusters"], update_tile_k=256)[1]
    label_path = folder / "compare-labels-torch.npy"
    import numpy as np

    np.save(label_path, labels.detach().cpu().numpy())
    result.update({"name": "compare-lloyd-step", "case": COMPARE, "phases": recorder.phases, "labels": str(label_path.name)})
    runs.append(result)
    payload["compare_case"] = COMPARE
    _save(path, payload)
    np.save(folder / "compare-X-seed.npy", np.array([0]))
    _ = samples_np, centroids_np
    return payload


def _plusplus(torch, folder):
    import numpy as np

    from kmeans_lloyd.iteration import kmeans_plusplus

    samples, _centroids = _feature_inputs(torch) if False else _host_inputs(torch, PLUSPLUS, seed=1)[:2]
    path = folder / "results.json"
    payload = json.loads(path.read_text()) if path.exists() else {"meta": _meta(torch)}
    print("start kmeans++", flush=True)
    result = _bench(
        lambda: kmeans_plusplus(samples, PLUSPLUS["n_clusters"], np.random.default_rng(1)),
        (),
        samples,
        warmup=1,
        repeats=1,
    )
    result.update({"name": "kmeans-plusplus", "case": PLUSPLUS})
    payload["plusplus"] = result
    print(f"done kmeans++ {result['median_seconds']:.4f}s peak {result['median_peak_extra_bytes']}", flush=True)
    _save(path, payload)


def _meta(torch):
    return {
        "host": platform.node(),
        "python": platform.python_version(),
        "torch": torch.__version__,
        "gpu": torch.cuda.get_device_name(0),
        "tf32": False,
    }


def _plot(folder):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    payload = json.loads((folder / "results.json").read_text())
    gemm = [row for row in payload.get("runs", []) if str(row.get("name", "")).startswith("gemm-") and row.get("status") == "ok"]
    if not gemm:
        return
    labels = [row["name"].replace("gemm-", "") for row in gemm]
    times = [row["median_seconds"] for row in gemm]
    peaks = [row["median_peak_extra_bytes"] / (1024**2) for row in gemm]
    fig, axes = plt.subplots(2, 1, figsize=(11, 7), sharex=True)
    axes[0].bar(labels, times, color="#2f5d50")
    axes[0].set_ylabel("median seconds")
    axes[0].set_title("Gram assignment tiles on feature-heavy")
    axes[1].bar(labels, peaks, color="#8c3a2f")
    axes[1].set_ylabel("peak extra MiB")
    axes[1].tick_params(axis="x", rotation=30)
    fig.tight_layout()
    fig.savefig(folder / "gemm-tiles.svg")
    print(f"wrote {folder / 'gemm-tiles.svg'}", flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("check", "tiles", "running", "profile", "lloyd", "plusplus", "plot"))
    args = parser.parse_args()
    torch = _configure_torch()
    if not torch.cuda.is_available():
        raise SystemExit("CUDA is required")
    folder = ROOT / "journal" / "004-tile-tradeoff"
    folder.mkdir(parents=True, exist_ok=True)
    if args.stage == "check":
        _check(torch)
        return
    if args.stage == "tiles":
        _check(torch)
        samples, centroids = _feature_inputs(torch)
        _run_gemm_tiles(torch, samples, centroids, folder)
        del samples, centroids
        _cleanup()
        return
    if args.stage == "running":
        samples, centroids = _feature_inputs(torch)
        _run_running(torch, samples, centroids, folder)
        return
    if args.stage == "profile":
        samples, centroids = _feature_inputs(torch)
        _profile(torch, samples, centroids, folder)
        return
    if args.stage == "lloyd":
        _lloyd(torch, folder)
        return
    if args.stage == "plusplus":
        _plusplus(torch, folder)
        return
    if args.stage == "plot":
        _plot(folder)


if __name__ == "__main__":
    main()
