"""Run Lloyd-iteration fusion experiments on CUDA.

Stages
------
probe
    Check the memory instrumentation, then compare eager execution with
    ``torch.compile`` and ``cupy.fuse`` on one medium problem that still
    fits the naive broadcast tensor.
bench
    Time and measure memory on three larger shapes. Naive broadcast is
    attempted only when the byte estimate leaves 20% of the GPU free.
"""

from __future__ import annotations

import argparse
import json
import platform
import sys
import time
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

# Disable TF32 before either library initializes cuBLAS so eager and
# compiled paths, and PyTorch and CuPy, share IEEE float32 matmul.
import os

os.environ.setdefault("NVIDIA_TF32_OVERRIDE", "0")

# Shapes are large enough for a GEMM assignment around a second on an L4,
# and small enough that eager execution can also form X * X (a full copy of
# the samples) plus the (n_samples, n_clusters) distance matrix and still
# leave about 20% of a 23 GiB GPU free.
CASES = [
    {
        "name": "sample-heavy",
        "n_samples": 131_072,
        "n_clusters": 8_192,
        "n_features": 8_192,
    },
    {
        "name": "centroid-heavy",
        "n_samples": 65_536,
        "n_clusters": 16_384,
        "n_features": 8_192,
    },
    {
        "name": "feature-heavy",
        "n_samples": 65_536,
        "n_clusters": 4_096,
        "n_features": 16_384,
    },
]

PROBE = {"name": "probe-broadcast", "n_samples": 4_096, "n_clusters": 256, "n_features": 512}


def _is_oom(exc):
    name = type(exc).__name__
    text = str(exc).lower()
    return "outofmemory" in name.lower() or "out of memory" in text


def _cleanup(backend):
    import gc

    gc.collect()
    if backend == "torch":
        import torch

        torch.cuda.synchronize()
        gc.collect()
        torch.cuda.empty_cache()
    elif backend == "cupy":
        import cupy

        cupy.cuda.Stream.null.synchronize()
        cupy.get_default_memory_pool().free_all_blocks()


def _device_memory(backend):
    if backend == "torch":
        import torch

        free, total = torch.cuda.mem_get_info()
        return int(free), int(total)
    import cupy

    free, total = cupy.cuda.runtime.memGetInfo()
    return int(free), int(total)


def _versions():
    info = {
        "python": platform.python_version(),
        "platform": platform.platform(),
    }
    try:
        import numpy

        info["numpy"] = numpy.__version__
    except Exception as exc:
        info["numpy_error"] = repr(exc)
    try:
        import array_api_compat

        info["array_api_compat"] = array_api_compat.__version__
    except Exception as exc:
        info["array_api_compat_error"] = repr(exc)
    try:
        import torch

        info["torch"] = torch.__version__
        info["torch_cuda"] = torch.version.cuda
        info["torch_gpu"] = torch.cuda.get_device_name(0) if torch.cuda.is_available() else None
        if torch.cuda.is_available():
            props = torch.cuda.get_device_properties(0)
            info["gpu_total_bytes"] = int(props.total_memory)
            info["tf32_matmul"] = bool(torch.backends.cuda.matmul.allow_tf32)
    except Exception as exc:
        info["torch_error"] = repr(exc)
    try:
        import cupy

        info["cupy"] = cupy.__version__
        info["cupy_runtime"] = int(cupy.cuda.runtime.runtimeGetVersion())
        info["cupy_gpu"] = cupy.cuda.runtime.getDeviceProperties(0)["name"].decode()
    except Exception as exc:
        info["cupy_error"] = repr(exc)
    return info


def _configure_torch():
    import torch

    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    try:
        torch.set_float32_matmul_precision("highest")
    except Exception:
        pass
    return torch


def _make_inputs(backend, case, seed=0):
    n = case["n_samples"]
    k = case["n_clusters"]
    d = case["n_features"]
    if backend == "torch":
        import torch

        generator = torch.Generator(device="cuda")
        generator.manual_seed(seed)
        x = torch.randn(n, d, device="cuda", dtype=torch.float32, generator=generator)
        pick = torch.randint(0, n, (k,), device="cuda", generator=generator)
        centroids = x.index_select(0, pick).contiguous()
        return x, centroids
    import cupy

    cupy.random.seed(seed)
    x = cupy.random.standard_normal((n, d), dtype=cupy.float32)
    pick = cupy.random.randint(0, n, size=(k,), dtype=cupy.int64)
    centroids = x[pick].copy()
    return x, centroids


def _bind(fn, xp, name):
    def wrapped(*args):
        return fn(xp, *args)

    wrapped.__name__ = name
    wrapped.__qualname__ = name
    return wrapped


def _xp_for(backend):
    if backend == "torch":
        import array_api_compat.torch as xp

        return xp
    import array_api_compat.cupy as xp

    return xp


def _median(values):
    ordered = sorted(values)
    mid = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[mid]
    return 0.5 * (ordered[mid - 1] + ordered[mid])


def _theory(case, itemsize=4):
    n = case["n_samples"]
    k = case["n_clusters"]
    d = case["n_features"]
    return {
        "broadcast_bytes": n * k * d * itemsize,
        "distance_bytes": n * k * itemsize,
        "labels_bytes": n * 8,
        "samples_bytes": n * d * itemsize,
        "centroids_bytes": k * d * itemsize,
        "gemm_flops": 2 * n * k * d,
    }


def _classify(peak_extra, case):
    theory = _theory(case)
    broadcast = theory["broadcast_bytes"]
    distance = theory["distance_bytes"]
    if peak_extra is None:
        return "unmeasured"
    if broadcast > 0 and peak_extra >= 0.5 * broadcast:
        return "materialized_broadcast"
    if distance > 0 and peak_extra >= 0.5 * distance:
        return "materialized_distance"
    if peak_extra <= max(theory["labels_bytes"] * 8, int(0.25 * distance) if distance else 0, 1 << 20):
        return "no_distance_matrix"
    return "between_labels_and_distance"


def _headroom_ok(backend, extra_bytes):
    free, total = _device_memory(backend)
    # Inputs are already allocated and included in `free`. Refuse a call
    # whose estimated temporary would leave under 20% of the card free.
    return free - extra_bytes >= 0.20 * total, free, total


def _bench(fn, args, example, warmup, repeats):
    from kmeans_lloyd.instrument import measure_call

    profiles = []
    output = None
    for index in range(warmup + repeats):
        output, profile = measure_call(fn, args, example)
        profile["warmup"] = index < warmup
        profile["iter"] = index
        profiles.append(profile)
        del output
    steady = [p for p in profiles if not p["warmup"]]
    return {
        "status": "ok",
        "median_seconds": _median([p["seconds"] for p in steady]),
        "min_seconds": min(p["seconds"] for p in steady),
        "median_peak_extra_bytes": int(_median([p["peak_extra_bytes"] for p in steady])),
        "median_retained_extra_bytes": int(_median([p["retained_extra_bytes"] for p in steady])),
        "profiles": profiles,
    }


def _compile_torch(fn, example_args):
    import torch

    torch._dynamo.reset()
    errors = []
    for fullgraph in (True, False):
        compiled = torch.compile(fn, fullgraph=fullgraph, backend="inductor")
        try:
            started = time.perf_counter()
            out = compiled(*example_args)
            torch.cuda.synchronize()
            compile_seconds = time.perf_counter() - started
            return compiled, {
                "fullgraph": fullgraph,
                "compile_seconds": compile_seconds,
                "error": None,
            }
        except Exception as exc:
            errors.append({"fullgraph": fullgraph, "error": f"{type(exc).__name__}: {exc}"})
            _cleanup("torch")
            torch._dynamo.reset()
    return None, {"fullgraph": None, "compile_seconds": None, "error": errors}


def _torch_kernels(fn, args):
    import torch
    from torch.profiler import ProfilerActivity, profile

    torch.cuda.synchronize()
    with profile(activities=[ProfilerActivity.CUDA], record_shapes=False) as prof:
        fn(*args)
        torch.cuda.synchronize()
    rows = []
    for event in prof.key_averages():
        device_time = getattr(event, "device_time_total", 0) or getattr(event, "self_device_time_total", 0)
        if not device_time:
            continue
        rows.append(
            {
                "name": event.key,
                "count": int(event.count),
                "device_time_us": float(device_time),
            }
        )
    rows.sort(key=lambda row: row["device_time_us"], reverse=True)
    return rows


def _try_cupy_fuse(fn, args, example):
    import cupy

    from kmeans_lloyd.instrument import measure_call

    fused = cupy.fuse(fn)
    try:
        started = time.perf_counter()
        out, profile = measure_call(fused, args, example)
        # The first call compiles the fused kernel. Time a second call.
        del out
        out, steady = measure_call(fused, args, example)
        del out
        return {
            "status": "ok",
            "compile_seconds": time.perf_counter() - started,
            "median_seconds": steady["seconds"],
            "median_peak_extra_bytes": steady["peak_extra_bytes"],
            "median_retained_extra_bytes": steady["retained_extra_bytes"],
            "error": None,
        }
    except Exception as exc:
        _cleanup("cupy")
        return {
            "status": "error",
            "error": f"{type(exc).__name__}: {exc}",
            "traceback": traceback.format_exc(limit=8),
        }


def _record(rows, **kwargs):
    rows.append(kwargs)
    status = kwargs.get("status")
    name = kwargs.get("name")
    seconds = kwargs.get("median_seconds")
    peak = kwargs.get("median_peak_extra_bytes")
    kind = kwargs.get("fusion")
    print(
        f"  {name}: status={status} time={seconds} peak_extra={peak} fusion={kind}",
        flush=True,
    )


def _run_pair(rows, backend, case, label, fn, args, example, warmup=1, repeats=3, kernels=False):
    theory = _theory(case)
    try:
        result = _bench(fn, args, example, warmup=warmup, repeats=repeats)
    except Exception as exc:
        _cleanup(backend)
        _record(
            rows,
            name=label,
            backend=backend,
            case=case["name"],
            mode="eager",
            status="oom" if _is_oom(exc) else "error",
            error=f"{type(exc).__name__}: {exc}",
            theory=theory,
        )
        return None
    result.update(
        {
            "name": label,
            "backend": backend,
            "case": case["name"],
            "mode": "eager",
            "fusion": _classify(result["median_peak_extra_bytes"], case),
            "theory": theory,
        }
    )
    if kernels and backend == "torch":
        try:
            result["kernels"] = _torch_kernels(fn, args)
        except Exception as exc:
            result["kernels_error"] = f"{type(exc).__name__}: {exc}"
    _record(rows, **{k: result[k] for k in ("name", "status", "median_seconds", "median_peak_extra_bytes", "fusion")})
    rows[-1] = result
    return fn


def _run_compiled_torch(rows, case, label, fn, args, example, warmup=1, repeats=3, kernels=True):
    compiled, meta = _compile_torch(fn, args)
    theory = _theory(case)
    if compiled is None:
        _record(
            rows,
            name=label,
            backend="torch",
            case=case["name"],
            mode="torch.compile",
            status="error",
            error=meta["error"],
            compile=meta,
            theory=theory,
        )
        return
    try:
        result = _bench(compiled, args, example, warmup=warmup, repeats=repeats)
    except Exception as exc:
        _cleanup("torch")
        _record(
            rows,
            name=label,
            backend="torch",
            case=case["name"],
            mode="torch.compile",
            status="oom" if _is_oom(exc) else "error",
            error=f"{type(exc).__name__}: {exc}",
            compile=meta,
            theory=theory,
        )
        return
    result.update(
        {
            "name": label,
            "backend": "torch",
            "case": case["name"],
            "mode": "torch.compile",
            "compile": meta,
            "fusion": _classify(result["median_peak_extra_bytes"], case),
            "theory": theory,
        }
    )
    if kernels:
        try:
            result["kernels"] = _torch_kernels(compiled, args)
        except Exception as exc:
            result["kernels_error"] = f"{type(exc).__name__}: {exc}"
    _record(
        rows,
        **{
            "name": label,
            "status": result["status"],
            "median_seconds": result["median_seconds"],
            "median_peak_extra_bytes": result["median_peak_extra_bytes"],
            "fusion": result["fusion"],
        },
    )
    rows[-1] = result


def _memory_self_test(backend, rows):
    """Allocate a known tensor and check that peak memory sees it."""
    import array_api_compat

    from kmeans_lloyd.instrument import measure_call

    xp = _xp_for(backend)
    n, m = 2048, 4096
    expected = n * m * 4
    if backend == "torch":
        import torch

        like = torch.empty(1, device="cuda")
    else:
        import cupy

        like = cupy.empty((1,), dtype=cupy.float32)

    def allocate(width):
        return xp.zeros((n, width), dtype=like.dtype, device=like.device)

    _, profile = measure_call(allocate, (m,), like)
    ratio = profile["peak_extra_bytes"] / expected
    status = "ok" if 0.8 <= ratio <= 1.5 else "error"
    _record(
        rows,
        name="memory-self-test",
        backend=backend,
        case="self-test",
        mode="eager",
        status=status,
        median_seconds=profile["seconds"],
        median_peak_extra_bytes=profile["peak_extra_bytes"],
        median_retained_extra_bytes=profile["retained_extra_bytes"],
        expected_bytes=expected,
        ratio=ratio,
        fusion="n/a",
        array_api_compat=array_api_compat.__version__,
    )
    if status != "ok":
        raise RuntimeError(f"{backend} memory self-test ratio {ratio:.3f} is outside [0.8, 1.5]")


def _elementwise_control(backend, rows):
    """A pointwise square-difference should fuse to a single output buffer."""
    from kmeans_lloyd.instrument import measure_call

    xp = _xp_for(backend)
    n, d = 1_048_576, 16
    if backend == "torch":
        import torch

        a = torch.randn(n, d, device="cuda")
        b = torch.randn(n, d, device="cuda")
    else:
        import cupy

        a = cupy.random.standard_normal((n, d), dtype=cupy.float32)
        b = cupy.random.standard_normal((n, d), dtype=cupy.float32)

    def sqdiff(left, right):
        diff = left - right
        return diff * diff

    case = {"name": "elementwise-control", "n_samples": n, "n_clusters": d, "n_features": 1}
    _, profile = measure_call(sqdiff, (a, b), a)
    _record(
        rows,
        name="elementwise-sqdiff",
        backend=backend,
        case=case["name"],
        mode="eager",
        status="ok",
        median_seconds=profile["seconds"],
        median_peak_extra_bytes=profile["peak_extra_bytes"],
        median_retained_extra_bytes=profile["retained_extra_bytes"],
        output_bytes=n * d * 4,
        fusion=_classify(profile["peak_extra_bytes"], {"n_samples": n, "n_clusters": d, "n_features": 2}),
    )
    if backend == "torch":
        _run_compiled_torch(
            rows,
            {"name": case["name"], "n_samples": n, "n_clusters": d, "n_features": 2},
            "elementwise-sqdiff",
            sqdiff,
            (a, b),
            a,
            kernels=True,
        )
    else:
        fused = _try_cupy_fuse(sqdiff, (a, b), a)
        fused.update(
            {
                "name": "elementwise-sqdiff",
                "backend": "cupy",
                "case": case["name"],
                "mode": "cupy.fuse",
                "output_bytes": n * d * 4,
            }
        )
        if fused.get("median_peak_extra_bytes") is not None:
            fused["fusion"] = _classify(
                fused["median_peak_extra_bytes"],
                {"n_samples": n, "n_clusters": d, "n_features": 2},
            )
        _record(
            rows,
            name=fused["name"],
            status=fused["status"],
            median_seconds=fused.get("median_seconds"),
            median_peak_extra_bytes=fused.get("median_peak_extra_bytes"),
            fusion=fused.get("fusion"),
        )
        rows[-1] = fused


def _probe_backend(backend, rows):
    print(f"\n== probe {backend} ==", flush=True)
    _memory_self_test(backend, rows)
    _elementwise_control(backend, rows)
    xp = _xp_for(backend)
    x, centroids = _make_inputs(backend, PROBE, seed=0)
    case = PROBE
    specs = [
        ("naive-argmin", _bind(__import__("kmeans_lloyd.iteration", fromlist=["broadcast_distance_argmin"]).broadcast_distance_argmin, xp, "broadcast_distance_argmin"), (x, centroids), case),
        ("distance-only", _bind(__import__("kmeans_lloyd.iteration", fromlist=["broadcast_distance_only"]).broadcast_distance_only, xp, "broadcast_distance_only"), (x, centroids), case),
        ("gemm-argmin", _bind(__import__("kmeans_lloyd.iteration", fromlist=["gemm_distance_argmin"]).gemm_distance_argmin, xp, "gemm_distance_argmin"), (x, centroids), case),
        (
            "one-centroid-distance",
            _bind(
                __import__("kmeans_lloyd.iteration", fromlist=["centroid_squared_distance"]).centroid_squared_distance,
                xp,
                "centroid_squared_distance",
            ),
            (x, centroids[0]),
            {"name": "probe-one-centroid", "n_samples": case["n_samples"], "n_clusters": 1, "n_features": case["n_features"]},
        ),
        (
            "running-step",
            _bind(
                __import__("kmeans_lloyd.iteration", fromlist=["running_argmin_step"]).running_argmin_step,
                xp,
                "running_argmin_step",
            ),
            (
                x,
                centroids[0],
                xp.full((x.shape[0],), xp.inf, dtype=x.dtype, device=x.device),
                xp.zeros(x.shape[0], dtype=xp.int64, device=x.device),
                xp.asarray(0, dtype=xp.int64, device=x.device),
            ),
            {"name": "probe-one-centroid", "n_samples": case["n_samples"], "n_clusters": 1, "n_features": case["n_features"]},
        ),
    ]
    # Import once, the __import__ above is just to keep the table local.
    for label, fn, args, spec_case in specs:
        print(f" eager {label}", flush=True)
        _run_pair(rows, backend, spec_case, label, fn, args, x, warmup=1, repeats=3, kernels=backend == "torch")
        if backend == "torch":
            print(f" compile {label}", flush=True)
            _run_compiled_torch(rows, spec_case, label, fn, args, x)
        else:
            print(f" fuse {label}", flush=True)
            fused = _try_cupy_fuse(fn, args, x)
            fused.update(
                {
                    "name": label,
                    "backend": "cupy",
                    "case": spec_case["name"],
                    "mode": "cupy.fuse",
                    "theory": _theory(spec_case),
                }
            )
            if fused.get("median_peak_extra_bytes") is not None:
                fused["fusion"] = _classify(fused["median_peak_extra_bytes"], spec_case)
            _record(
                rows,
                name=label,
                status=fused["status"],
                median_seconds=fused.get("median_seconds"),
                median_peak_extra_bytes=fused.get("median_peak_extra_bytes"),
                fusion=fused.get("fusion"),
            )
            rows[-1] = fused

    # Tile sweep: does a smaller broadcast region change the fusion class?
    from kmeans_lloyd.iteration import tile_broadcast_argmin

    tile_fn = _bind(tile_broadcast_argmin, xp, "tile_broadcast_argmin")
    for tile_k in (16, 64, 256):
        tile_case = {
            "name": f"probe-tile-k{tile_k}",
            "n_samples": case["n_samples"],
            "n_clusters": tile_k,
            "n_features": case["n_features"],
        }
        args = (x, centroids[:tile_k])
        label = f"tile-broadcast-k{tile_k}"
        _run_pair(rows, backend, tile_case, label, tile_fn, args, x, kernels=backend == "torch")
        if backend == "torch":
            _run_compiled_torch(rows, tile_case, label, tile_fn, args, x)
        else:
            fused = _try_cupy_fuse(tile_fn, args, x)
            fused.update(
                {
                    "name": label,
                    "backend": "cupy",
                    "case": tile_case["name"],
                    "mode": "cupy.fuse",
                    "theory": _theory(tile_case),
                }
            )
            if fused.get("median_peak_extra_bytes") is not None:
                fused["fusion"] = _classify(fused["median_peak_extra_bytes"], tile_case)
            rows.append(fused)
            print(f"  {label} fuse status={fused['status']}", flush=True)
    _running_loop_probe(backend, rows)
    del x, centroids
    _cleanup(backend)


def _running_loop_probe(backend, rows):
    """Compile the Python loop over centroids, not only one step.

    The single-centroid body fuses under torch.compile. This checks whether
    the loop over a handful of centroids becomes one kernel or stays one
    launch per centroid.
    """
    from kmeans_lloyd.iteration import assign_running

    for k in (8, 32):
        case = {
            "name": f"probe-running-loop-k{k}",
            "n_samples": 4_096,
            "n_clusters": k,
            "n_features": 512,
        }
        x, centroids = _make_inputs(backend, case, seed=4)
        print(f" running-loop k={k}", flush=True)
        _run_pair(rows, backend, case, f"running-loop-k{k}", assign_running, (x, centroids), x, kernels=backend == "torch")
        if backend == "torch":
            _run_compiled_torch(rows, case, f"running-loop-k{k}", assign_running, (x, centroids), x)
        else:
            fused = _try_cupy_fuse(assign_running, (x, centroids), x)
            fused.update(
                {
                    "name": f"running-loop-k{k}",
                    "backend": "cupy",
                    "case": case["name"],
                    "mode": "cupy.fuse",
                    "theory": _theory(case),
                }
            )
            if fused.get("median_peak_extra_bytes") is not None:
                fused["fusion"] = _classify(fused["median_peak_extra_bytes"], case)
            rows.append(fused)
            print(f"  running-loop k={k} fuse status={fused['status']}", flush=True)
        del x, centroids
        _cleanup(backend)


def _bench_compiled_running_tiles(rows, case, x, centroids):
    """Time a fused running-argmin tile, then the full assignment if it is cheap.

    ``torch.compile`` turns ``running_tile_distances`` into one kernel when
    the tile has a few dozen centroids. A Python loop over those tiles covers
    a large cluster count without unrolling it into one giant compile.
    """
    from kmeans_lloyd.iteration import assign_running_tiled, running_tile_distances

    tile_k = 32
    if int(centroids.shape[0]) < tile_k:
        return
    tile = centroids[:tile_k]
    tile_case = {
        "name": case["name"] + f"-running-tile-k{tile_k}",
        "n_samples": case["n_samples"],
        "n_clusters": tile_k,
        "n_features": case["n_features"],
    }
    _run_pair(rows, "torch", tile_case, "running-tile", running_tile_distances, (x, tile), x, kernels=True)
    _run_compiled_torch(
        rows,
        tile_case,
        "running-tile",
        running_tile_distances,
        (x, tile),
        x,
        warmup=0,
        repeats=2,
    )
    compiled_rows = [
        row
        for row in rows
        if row.get("name") == "running-tile"
        and row.get("mode") == "torch.compile"
        and row.get("case") == tile_case["name"]
        and row.get("status") == "ok"
    ]
    if not compiled_rows:
        return
    per_tile = compiled_rows[-1]["median_seconds"]
    n_tiles = int(centroids.shape[0]) / tile_k
    estimate = per_tile * n_tiles
    if estimate > 20:
        _record(
            rows,
            name="running-tiled-full",
            backend="torch",
            case=case["name"],
            mode="torch.compile",
            status="skipped_estimate",
            median_seconds=None,
            estimated_seconds=estimate,
            fusion="not_run",
            theory=_theory(case),
        )
        return
    compiled = torch_compile_cached(running_tile_distances)

    def full_assign():
        return assign_running_tiled(x, centroids, tile_k=tile_k, block=compiled)

    try:
        result = _bench(full_assign, (), x, warmup=0, repeats=1)
    except Exception as exc:
        _cleanup("torch")
        _record(
            rows,
            name="running-tiled-full",
            backend="torch",
            case=case["name"],
            mode="torch.compile",
            status="oom" if _is_oom(exc) else "error",
            error=f"{type(exc).__name__}: {exc}",
            theory=_theory(case),
        )
        return
    result.update(
        {
            "name": "running-tiled-full",
            "backend": "torch",
            "case": case["name"],
            "mode": "torch.compile",
            "status": "ok",
            "fusion": _classify(result["median_peak_extra_bytes"], case),
            "theory": _theory(case),
            "tile_k": tile_k,
            "estimated_from_one_tile_seconds": estimate,
        }
    )
    _record(
        rows,
        name="running-tiled-full",
        status="ok",
        median_seconds=result["median_seconds"],
        median_peak_extra_bytes=result["median_peak_extra_bytes"],
        fusion=result["fusion"],
    )
    rows[-1] = result


def torch_compile_cached(fn):
    import torch

    compiled = getattr(fn, "_kmeans_compiled", None)
    if compiled is None:
        compiled = torch.compile(fn, fullgraph=False)
        fn._kmeans_compiled = compiled
    return compiled


def _full_iteration(backend, case, assign, rows, **kwargs):
    from kmeans_lloyd.iteration import assign_gemm, assign_naive, update_centroids
    from kmeans_lloyd.instrument import measure_call

    estimate = _theory(case)
    temporary = estimate["distance_bytes"]
    if assign == "naive":
        temporary = estimate["broadcast_bytes"]
    ok, free, total = _headroom_ok(backend, temporary)
    label = f"lloyd-{assign}"
    if not ok:
        _record(
            rows,
            name=label,
            backend=backend,
            case=case["name"],
            mode="eager",
            status="skipped_headroom",
            median_seconds=None,
            median_peak_extra_bytes=None,
            fusion="not_run",
            theory=estimate,
            free_bytes=free,
            total_bytes=total,
            estimated_temporary_bytes=temporary,
        )
        return

    x, centroids = _make_inputs(backend, case, seed=1)
    assign_fn = {"gemm": assign_gemm, "naive": assign_naive}[assign]
    held = {}

    def assign_keep():
        held["labels"] = assign_fn(x, centroids)
        return held["labels"]

    try:
        profiles = []
        for index in range(1 + 3):
            _, assign_profile = measure_call(assign_keep, (), x)
            labels = held["labels"]
            # The assignment's distance temporary is still in the caching
            # allocator. Release it before timing the mean update.
            del held["labels"]
            _cleanup(backend)
            _, update_profile = measure_call(
                lambda labs: update_centroids(x, labs, centroids),
                (labels,),
                x,
            )
            profiles.append(
                {
                    "warmup": index == 0,
                    "assign_seconds": assign_profile["seconds"],
                    "update_seconds": update_profile["seconds"],
                    "assign_peak_extra_bytes": assign_profile["peak_extra_bytes"],
                    "update_peak_extra_bytes": update_profile["peak_extra_bytes"],
                    "total_seconds": assign_profile["seconds"] + update_profile["seconds"],
                }
            )
            del labels
    except Exception as exc:
        _cleanup(backend)
        _record(
            rows,
            name=label,
            backend=backend,
            case=case["name"],
            mode="eager",
            status="oom" if _is_oom(exc) else "error",
            error=f"{type(exc).__name__}: {exc}",
            theory=estimate,
        )
        del x, centroids
        return
    steady = [p for p in profiles if not p["warmup"]]
    result = {
        "name": label,
        "backend": backend,
        "case": case["name"],
        "mode": "eager",
        "status": "ok",
        "assign": assign,
        "assign_kwargs": kwargs,
        "median_seconds": _median([p["total_seconds"] for p in steady]),
        "median_assign_seconds": _median([p["assign_seconds"] for p in steady]),
        "median_update_seconds": _median([p["update_seconds"] for p in steady]),
        "median_peak_extra_bytes": int(_median([p["assign_peak_extra_bytes"] for p in steady])),
        "median_update_peak_extra_bytes": int(_median([p["update_peak_extra_bytes"] for p in steady])),
        "fusion": _classify(_median([p["assign_peak_extra_bytes"] for p in steady]), case),
        "profiles": profiles,
        "theory": estimate,
    }
    _record(
        rows,
        name=label,
        status="ok",
        median_seconds=result["median_seconds"],
        median_peak_extra_bytes=result["median_peak_extra_bytes"],
        fusion=result["fusion"],
    )
    rows[-1] = result
    del x, centroids
    _cleanup(backend)


def _bench_assignment(backend, rows):
    """Eager vs compiled assignment on the three shapes, plus tiled rewrites."""
    from kmeans_lloyd.iteration import (
        gemm_distance_argmin,
        running_argmin_step,
        tile_broadcast_argmin,
        tile_gemm_argmin,
    )

    xp = _xp_for(backend)
    gemm_fn = _bind(gemm_distance_argmin, xp, "gemm_distance_argmin")
    tile_b = _bind(tile_broadcast_argmin, xp, "tile_broadcast_argmin")
    tile_g = _bind(tile_gemm_argmin, xp, "tile_gemm_argmin")
    running = _bind(running_argmin_step, xp, "running_argmin_step")

    for case in CASES:
        print(f"\n== bench {backend} {case['name']} ==", flush=True)
        _cleanup(backend)
        ok, free, total = _headroom_ok(backend, _theory(case)["samples_bytes"] + _theory(case)["centroids_bytes"])
        if not ok:
            _record(
                rows,
                name="inputs",
                backend=backend,
                case=case["name"],
                mode="eager",
                status="skipped_headroom",
                free_bytes=free,
                total_bytes=total,
                fusion="not_run",
            )
            continue
        x, centroids = _make_inputs(backend, case, seed=2)
        _run_pair(rows, backend, case, "gemm-argmin", gemm_fn, (x, centroids), x, warmup=1, repeats=3, kernels=True)
        if backend == "torch":
            _run_compiled_torch(rows, case, "gemm-argmin", gemm_fn, (x, centroids), x, warmup=1, repeats=3)

        # One broadcast tile small enough that the unfused (tile_n, tile_k, d) tensor fits.
        tile_k = 32
        tile_bytes_target = 256 * 2**20
        tile_n = max(32, tile_bytes_target // (tile_k * case["n_features"] * 4))
        tile_n = min(tile_n, int(x.shape[0]))
        tile_case = {
            "name": case["name"] + f"-broadcast-tile-{tile_n}x{tile_k}",
            "n_samples": tile_n,
            "n_clusters": tile_k,
            "n_features": case["n_features"],
        }
        xb = x[:tile_n]
        cb = centroids[:tile_k]
        _run_pair(rows, backend, tile_case, "broadcast-tile", tile_b, (xb, cb), x, kernels=True)
        if backend == "torch":
            _run_compiled_torch(rows, tile_case, "broadcast-tile", tile_b, (xb, cb), x)
        else:
            fused = _try_cupy_fuse(tile_b, (xb, cb), x)
            fused.update({"name": "broadcast-tile", "backend": "cupy", "case": tile_case["name"], "mode": "cupy.fuse", "theory": _theory(tile_case)})
            if fused.get("median_peak_extra_bytes") is not None:
                fused["fusion"] = _classify(fused["median_peak_extra_bytes"], tile_case)
            rows.append(fused)

        # Gram tile over samples, full centroid count, so the distance tile is the fusion target.
        gemm_tile_n = min(4096, int(x.shape[0]))
        gemm_tile_case = {
            "name": case["name"] + f"-gemm-tile-n{gemm_tile_n}",
            "n_samples": gemm_tile_n,
            "n_clusters": case["n_clusters"],
            "n_features": case["n_features"],
        }
        distance_bytes = gemm_tile_n * case["n_clusters"] * 4
        ok_tile, _, _ = _headroom_ok(backend, distance_bytes)
        if ok_tile:
            _run_pair(
                rows,
                backend,
                gemm_tile_case,
                "gemm-tile",
                tile_g,
                (x[:gemm_tile_n], centroids),
                x,
                kernels=True,
            )
            if backend == "torch":
                _run_compiled_torch(
                    rows,
                    gemm_tile_case,
                    "gemm-tile",
                    tile_g,
                    (x[:gemm_tile_n], centroids),
                    x,
                )

        # A handful of running-argmin steps. Full k would re-read X once per centroid.
        steps = 4
        best_dist = xp.full((x.shape[0],), xp.inf, dtype=x.dtype, device=x.device)
        best_idx = xp.zeros(x.shape[0], dtype=xp.int64, device=x.device)
        index = xp.asarray(0, dtype=xp.int64, device=x.device)
        step_case = {
            "name": case["name"] + "-running-step",
            "n_samples": case["n_samples"],
            "n_clusters": 1,
            "n_features": case["n_features"],
        }
        _run_pair(
            rows,
            backend,
            step_case,
            f"running-step-x{steps}",
            _Repeat(running, steps),
            (x, centroids[0], best_dist, best_idx, index),
            x,
            kernels=backend == "torch",
        )
        if backend == "torch":
            _run_compiled_torch(
                rows,
                step_case,
                "running-step",
                running,
                (x, centroids[0], best_dist, best_idx, index),
                x,
            )
        else:
            fused = _try_cupy_fuse(running, (x, centroids[0], best_dist, best_idx, index), x)
            fused.update(
                {
                    "name": "running-step",
                    "backend": "cupy",
                    "case": step_case["name"],
                    "mode": "cupy.fuse",
                    "theory": _theory(step_case),
                }
            )
            if fused.get("median_peak_extra_bytes") is not None:
                fused["fusion"] = _classify(fused["median_peak_extra_bytes"], step_case)
            rows.append(fused)
            print(f"  running-step fuse status={fused['status']}", flush=True)

        if backend == "torch":
            _bench_compiled_running_tiles(rows, case, x, centroids)
        del x, centroids, best_dist, best_idx
        _cleanup(backend)
        _full_iteration(backend, case, "gemm", rows)
        _full_iteration(backend, case, "naive", rows)


class _Repeat:
    """Call a step function several times so the timed region is not a single launch."""

    def __init__(self, fn, times):
        self.fn = fn
        self.times = times
        self.__name__ = fn.__name__

    def __call__(self, *args):
        out = None
        for _ in range(self.times):
            out = self.fn(*args)
        return out


def _write(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, default=str) + "\n")
    print(f"wrote {path}", flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("probe", "bench", "all"))
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()
    out = args.out
    if out is None:
        out = ROOT / "journal" / ("001-fusion-probe" if args.stage == "probe" else "002-three-shapes")
        if args.stage == "all":
            out = ROOT / "journal" / "003-combined"
    rows = []
    meta = _versions()
    print(json.dumps(meta, indent=2, default=str), flush=True)
    if "torch" in meta:
        _configure_torch()
    backends = []
    if "torch" in meta and meta.get("torch_gpu"):
        backends.append("torch")
    if "cupy" in meta and "cupy_error" not in meta:
        backends.append("cupy")
    if not backends:
        raise SystemExit("no CUDA backend imported")
    try:
        if args.stage in ("probe", "all"):
            for backend in backends:
                _probe_backend(backend, rows)
        if args.stage in ("bench", "all"):
            for backend in backends:
                _bench_assignment(backend, rows)
    finally:
        payload = {"meta": meta, "cases": CASES, "probe": PROBE, "runs": rows}
        _write(out / "results.json", payload)


if __name__ == "__main__":
    main()
