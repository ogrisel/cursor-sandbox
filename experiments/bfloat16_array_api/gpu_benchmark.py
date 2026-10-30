# Authors: The scikit-learn developers
# SPDX-License-Identifier: BSD-3-Clause

"""Contention-aware CUDA benchmark for bfloat16 Array API inputs."""

from __future__ import annotations

import argparse
import json
import os
import platform
import subprocess
import sys
import time
from pathlib import Path

os.environ.setdefault("SCIPY_ARRAY_API", "1")

import numpy as np
import torch
from benchmark import as_numpy, make_data, model_nbytes

import sklearn
from sklearn import config_context
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import accuracy_score, r2_score
from sklearn.model_selection import KFold, StratifiedKFold
from sklearn.naive_bayes import GaussianNB

GPU_CASES = {
    "GaussianNB": (6_400_000, 128),
    "LogisticRegression": (3_600_000, 256),
    "Ridge": (300_000, 512),
}


def gpu_snapshot():
    fields = (
        "utilization.gpu,memory.used,memory.free,memory.total,"
        "temperature.gpu,power.draw"
    )
    output = subprocess.check_output(
        [
            "nvidia-smi",
            f"--query-gpu={fields}",
            "--format=csv,noheader,nounits",
        ],
        text=True,
    )
    values = [float(value.strip()) for value in output.strip().split(",")]
    return dict(
        zip(
            (
                "utilization_pct",
                "memory_used_mb",
                "memory_free_mb",
                "memory_total_mb",
                "temperature_c",
                "power_w",
            ),
            values,
        )
    )


def external_gpu_processes():
    output = subprocess.run(
        [
            "nvidia-smi",
            "--query-compute-apps=pid,used_memory",
            "--format=csv,noheader,nounits",
        ],
        check=True,
        text=True,
        capture_output=True,
    ).stdout
    processes = []
    for line in output.splitlines():
        pid, used_memory = (part.strip() for part in line.split(","))
        if int(pid) != os.getpid():
            processes.append({"pid": int(pid), "used_memory_mb": float(used_memory)})
    return processes


def synchronize():
    torch.cuda.synchronize()


def wait_for_idle_gpu(*, minimum_free_mb, stable_samples, interval_s, timeout_s):
    """Wait for several consecutive low-utilization samples."""
    deadline = time.monotonic() + timeout_s
    consecutive = 0
    while time.monotonic() < deadline:
        snapshot = gpu_snapshot()
        print(json.dumps({"status": "waiting", "snapshot": snapshot}), flush=True)
        if (
            snapshot["utilization_pct"] <= 10
            and snapshot["memory_free_mb"] >= minimum_free_mb
        ):
            consecutive += 1
            if consecutive >= stable_samples:
                return
        else:
            consecutive = 0
        time.sleep(interval_s)
    raise TimeoutError("GPU did not reach a stable idle state before the timeout")


def take_rows(array, indices):
    indices = torch.asarray(indices, dtype=torch.int64, device=array.device)
    return array[indices]


def make_estimator(name):
    if name == "GaussianNB":
        return GaussianNB()
    if name == "LogisticRegression":
        return LogisticRegression(solver="lbfgs", max_iter=100, tol=1e-4)
    return Ridge(solver="svd", alpha=1.0)


def worker(estimator_name, dtype, repeat):
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is not available")

    before = gpu_snapshot()
    neighbors_before = external_gpu_processes()
    if before["utilization_pct"] > 10:
        print(
            json.dumps(
                {
                    "status": "contended",
                    "stage": "before",
                    "snapshot": before,
                    "external_processes": neighbors_before,
                }
            )
        )
        return

    n_samples, n_features = GPU_CASES[estimator_name]
    X_numpy, y_numpy = make_data(estimator_name, n_samples, n_features)
    torch_dtype = torch.float32 if dtype == "float32" else torch.bfloat16
    X = torch.asarray(X_numpy, dtype=torch_dtype, device="cuda")
    y_dtype = torch_dtype if np.issubdtype(y_numpy.dtype, np.floating) else torch.int64
    y = torch.asarray(y_numpy, dtype=y_dtype, device="cuda")
    del X_numpy

    free_bytes, total_bytes = torch.cuda.mem_get_info()
    if free_bytes < 0.3 * total_bytes:
        print(
            json.dumps(
                {
                    "status": "insufficient_headroom",
                    "free_mb": free_bytes / 2**20,
                    "total_mb": total_bytes / 2**20,
                }
            )
        )
        return

    splitter = (
        KFold(3, shuffle=True, random_state=repeat)
        if estimator_name == "Ridge"
        else StratifiedKFold(3, shuffle=True, random_state=repeat)
    )
    torch.cuda.reset_peak_memory_stats()
    fit_times = []
    predict_times = []
    scores = []
    fitted_bytes = []
    fold_snapshots = []

    for train, test in splitter.split(np.empty(n_samples), y_numpy):
        snapshot = gpu_snapshot()
        neighbors = external_gpu_processes()
        fold_snapshots.append(snapshot)
        if snapshot["utilization_pct"] > 10 and neighbors:
            print(
                json.dumps(
                    {
                        "status": "contended",
                        "stage": "between_folds",
                        "snapshot": snapshot,
                        "external_processes": neighbors,
                    }
                )
            )
            return

        X_train, X_test = take_rows(X, train), take_rows(X, test)
        y_train = take_rows(y, train)
        estimator = make_estimator(estimator_name)
        with config_context(array_api_dispatch=True):
            synchronize()
            start = time.perf_counter()
            estimator.fit(X_train, y_train)
            synchronize()
            fit_times.append(time.perf_counter() - start)

            start = time.perf_counter()
            prediction = estimator.predict(X_test)
            synchronize()
            predict_times.append(time.perf_counter() - start)

        prediction = as_numpy(prediction)
        score = (
            r2_score(y_numpy[test], prediction)
            if estimator_name == "Ridge"
            else accuracy_score(y_numpy[test], prediction)
        )
        scores.append(score)
        fitted_bytes.append(model_nbytes(estimator))
        del X_train, X_test, y_train, prediction, estimator
        torch.cuda.empty_cache()

    after = gpu_snapshot()
    neighbors_after = external_gpu_processes()
    minimum_free_mb = min(
        snapshot["memory_free_mb"] for snapshot in [before, *fold_snapshots, after]
    )
    conservative_min_free_mb = min(
        minimum_free_mb,
        before["memory_free_mb"] - torch.cuda.max_memory_allocated() / 2**20,
    )
    has_headroom = conservative_min_free_mb >= 0.2 * before["memory_total_mb"]
    result = {
        "status": "ok" if has_headroom else "insufficient_headroom",
        "estimator": estimator_name,
        "backend": "torch_cuda",
        "dtype": dtype,
        "repeat": repeat,
        "n_samples": n_samples,
        "n_features": n_features,
        "input_mb": X.nelement() * X.element_size() / 2**20,
        "fit_s": float(np.sum(fit_times)),
        "predict_s": float(np.sum(predict_times)),
        "score_mean": float(np.mean(scores)),
        "score_std": float(np.std(scores)),
        "model_kb": float(np.mean(fitted_bytes) / 2**10),
        "gpu_peak_allocated_mb": torch.cuda.max_memory_allocated() / 2**20,
        "gpu_min_free_mb": conservative_min_free_mb,
        "gpu_total_mb": before["memory_total_mb"],
        "before": before,
        "after": after,
        "external_processes_before": neighbors_before,
        "external_processes_after": neighbors_after,
    }
    print(json.dumps(result))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--estimator", choices=GPU_CASES)
    parser.add_argument("--dtype", choices=("float32", "bfloat16"))
    parser.add_argument("--repeat", type=int, default=0)
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--max-attempts", type=int, default=5)
    parser.add_argument("--minimum-free-mb", type=float, default=8_000)
    parser.add_argument("--idle-samples", type=int, default=3)
    parser.add_argument("--idle-interval-s", type=float, default=2)
    parser.add_argument("--idle-timeout-s", type=float, default=1_800)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("experiments/bfloat16_array_api/results/gpu_results.json"),
    )
    args = parser.parse_args()

    if args.worker:
        worker(args.estimator, args.dtype, args.repeat)
        return

    results = []
    rejected = []
    for estimator_name in GPU_CASES:
        for dtype in ("float32", "bfloat16"):
            repeat = 0
            attempts = 0
            while repeat < args.repeats and attempts < args.max_attempts:
                wait_for_idle_gpu(
                    minimum_free_mb=args.minimum_free_mb,
                    stable_samples=args.idle_samples,
                    interval_s=args.idle_interval_s,
                    timeout_s=args.idle_timeout_s,
                )
                command = [
                    sys.executable,
                    __file__,
                    "--worker",
                    "--estimator",
                    estimator_name,
                    "--dtype",
                    dtype,
                    "--repeat",
                    str(repeat),
                ]
                completed = subprocess.run(
                    command, check=True, text=True, capture_output=True
                )
                result = json.loads(completed.stdout.splitlines()[-1])
                print(json.dumps(result), flush=True)
                attempts += 1
                if result["status"] == "ok":
                    results.append(result)
                    repeat += 1
                else:
                    rejected.append(result)
                    time.sleep(15)

            if repeat < args.repeats:
                raise RuntimeError(
                    f"Could not collect {args.repeats} clean repeats for "
                    f"{estimator_name} {dtype}"
                )

    payload = {
        "metadata": {
            "platform": platform.platform(),
            "python": platform.python_version(),
            "sklearn": sklearn.__version__,
            "numpy": np.__version__,
            "torch": torch.__version__,
            "gpu": torch.cuda.get_device_name(),
            "cv_folds": 3,
            "repeats": args.repeats,
            "headroom_policy": (
                f"at least {args.minimum_free_mb:.0f} MiB free before each worker "
                "and 20% conservative free headroom during each run"
            ),
        },
        "results": results,
        "rejected_runs": rejected,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n")


if __name__ == "__main__":
    main()
