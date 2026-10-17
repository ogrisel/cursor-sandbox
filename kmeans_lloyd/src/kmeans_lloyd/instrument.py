"""Timing and device-memory measurements for one array-API call.

Peak memory is the quantity that tells fusion apart from a faster schedule:
a fused argmin never allocates the distance matrix, and a fused broadcast
never allocates the ``(n, k, d)`` difference tensor.
"""

from __future__ import annotations

from contextlib import contextmanager


def array_backend(array):
    """Return ``"torch"``, ``"cupy"``, or ``"numpy"`` for an array object."""
    module = type(array).__module__
    if module.startswith("torch"):
        return "torch"
    if module.startswith("cupy"):
        return "cupy"
    return "numpy"


class PhaseRecorder:
    """Collect per-phase timing and memory while a Lloyd iteration runs."""

    def __init__(self, example):
        self.example = example
        self.phases = []

    @contextmanager
    def phase(self, name):
        token = _start(self.example)
        try:
            yield
        finally:
            profile = _stop(self.example, token)
            profile["phase"] = name
            self.phases.append(profile)


def measure_call(fn, args, example):
    """Run ``fn(*args)`` and return ``(output, profile)``.

    The device timer and the CuPy memory hook are always closed, including
    when ``fn`` raises. CuPy allows only one memory hook at a time.
    """
    token = _start(example)
    try:
        output = fn(*args)
    finally:
        profile = _stop(example, token)
    return output, profile


def _start(example):
    backend = array_backend(example)
    if backend == "torch":
        import torch

        torch.cuda.synchronize()
        torch.cuda.reset_peak_memory_stats()
        start = torch.cuda.Event(enable_timing=True)
        end = torch.cuda.Event(enable_timing=True)
        start.record()
        return {
            "backend": backend,
            "before": torch.cuda.memory_allocated(),
            "start": start,
            "end": end,
        }
    if backend == "cupy":
        import cupy

        cupy.cuda.Stream.null.synchronize()
        pool = cupy.get_default_memory_pool()
        before = pool.used_bytes()
        hook = _CuPyPeakHook(before)
        hook.__enter__()
        start = cupy.cuda.Event()
        end = cupy.cuda.Event()
        start.record()
        return {
            "backend": backend,
            "before": before,
            "start": start,
            "end": end,
            "hook": hook,
        }
    from time import perf_counter

    return {"backend": backend, "t0": perf_counter()}


def _stop(example, token):
    backend = token["backend"]
    if backend == "torch":
        token["end"].record()
        token["end"].synchronize()
        import torch

        peak = torch.cuda.max_memory_allocated()
        after = torch.cuda.memory_allocated()
        return {
            "backend": backend,
            "seconds": token["start"].elapsed_time(token["end"]) / 1000.0,
            "peak_extra_bytes": int(peak - token["before"]),
            "retained_extra_bytes": int(after - token["before"]),
        }
    if backend == "cupy":
        import cupy

        seconds = None
        try:
            token["end"].record()
            token["end"].synchronize()
            seconds = cupy.cuda.get_elapsed_time(token["start"], token["end"]) / 1000.0
        finally:
            token["hook"].__exit__(None, None, None)
        after = cupy.get_default_memory_pool().used_bytes()
        return {
            "backend": backend,
            "seconds": seconds,
            "peak_extra_bytes": int(token["hook"].peak_used - token["before"]),
            "retained_extra_bytes": int(after - token["before"]),
        }
    from time import perf_counter

    return {
        "backend": backend,
        "seconds": perf_counter() - token["t0"],
        "peak_extra_bytes": None,
        "retained_extra_bytes": None,
    }


class _CuPyPeakHook:
    """Sample the pooling allocator at every checkout.

    CuPy has no peak-memory counter. Sampling ``used_bytes`` inside the
    alloc hook catches tensors that are freed before the call returns.
    """

    def __init__(self, before_used):
        import cupy

        self.peak_used = before_used
        self._hook = _hook_class()(self)

    def __enter__(self):
        self._hook.__enter__()
        return self

    def __exit__(self, exc_type, exc, tb):
        return self._hook.__exit__(exc_type, exc, tb)


def _hook_class():
    import cupy

    class PeakMemoryHook(cupy.cuda.MemoryHook):
        def __init__(self, tracker):
            super().__init__()
            self.tracker = tracker

        def malloc_postprocess(self, **kwargs):
            # malloc is a checkout from the pool (an array allocation).
            # alloc_* only fires when the pool itself grows.
            used = cupy.get_default_memory_pool().used_bytes()
            if used > self.tracker.peak_used:
                self.tracker.peak_used = used

    return PeakMemoryHook
