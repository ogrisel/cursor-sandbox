# Authors: The scikit-learn developers
# SPDX-License-Identifier: BSD-3-Clause

"""Benchmark bfloat16 Array API inputs for selected scikit-learn estimators."""

from __future__ import annotations

import argparse
import ctypes
import gc
import json
import os
import platform
import subprocess
import sys
import threading
import time
from pathlib import Path

os.environ.setdefault("SCIPY_ARRAY_API", "1")
os.environ.setdefault("OMP_NUM_THREADS", "4")
os.environ.setdefault("MKL_NUM_THREADS", "4")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "4")

import ml_dtypes
import numpy as np
import psutil
import torch
from threadpoolctl import threadpool_limits

import sklearn
from sklearn import config_context
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import accuracy_score, r2_score
from sklearn.model_selection import KFold, StratifiedKFold
from sklearn.naive_bayes import GaussianNB

CASES = {
    "GaussianNB": (800_000, 128),
    "LogisticRegression": (400_000, 256),
    "Ridge": (30_000, 512),
}


def _trim_allocator():
    gc.collect()
    try:
        ctypes.CDLL("libc.so.6").malloc_trim(0)
    except (AttributeError, OSError):
        pass


class PeakRSS:
    def __init__(self):
        self.process = psutil.Process()
        self.peak = self.process.memory_info().rss
        self._stop = threading.Event()

    def __enter__(self):
        def sample():
            while not self._stop.wait(0.002):
                self.peak = max(self.peak, self.process.memory_info().rss)

        self._thread = threading.Thread(target=sample, daemon=True)
        self._thread.start()
        return self

    def __exit__(self, *_):
        self._stop.set()
        self._thread.join()
        self.peak = max(self.peak, self.process.memory_info().rss)


def make_data(estimator_name, n_samples, n_features):
    rng = np.random.default_rng(0)
    X = rng.standard_normal((n_samples, n_features), dtype=np.float32)
    if estimator_name == "Ridge":
        coef = rng.standard_normal(n_features, dtype=np.float32)
        y = X @ coef + rng.standard_normal(n_samples, dtype=np.float32) * 0.2
    else:
        signal = X[:, :8].sum(axis=1)
        y = (signal + rng.standard_normal(n_samples, dtype=np.float32) > 0).astype(
            np.int64
        )
        if estimator_name == "GaussianNB":
            X += y[:, None] * np.float32(0.35)
    return X, y


def convert_data(X, y, backend, dtype):
    if backend == "numpy":
        target_dtype = np.float32 if dtype == "float32" else ml_dtypes.bfloat16
        return X.astype(target_dtype, copy=False), y

    target_dtype = torch.float32 if dtype == "float32" else torch.bfloat16
    X = torch.asarray(X).to(dtype=target_dtype)
    y_dtype = target_dtype if np.issubdtype(y.dtype, np.floating) else torch.int64
    return X, torch.asarray(y, dtype=y_dtype)


def take_rows(array, indices):
    if isinstance(array, torch.Tensor):
        indices = torch.asarray(indices, dtype=torch.int64)
    return array[indices]


def nbytes(array):
    if isinstance(array, torch.Tensor):
        return array.nelement() * array.element_size()
    return array.nbytes


def model_nbytes(estimator):
    total = 0
    for value in vars(estimator).values():
        if isinstance(value, torch.Tensor):
            total += value.nelement() * value.element_size()
        elif isinstance(value, np.ndarray):
            total += value.nbytes
    return total


def as_numpy(array):
    if isinstance(array, torch.Tensor):
        return array.detach().cpu().to(dtype=torch.float32).numpy()
    return np.asarray(array)


def make_estimator(name):
    if name == "GaussianNB":
        return GaussianNB()
    if name == "LogisticRegression":
        return LogisticRegression(solver="lbfgs", max_iter=100, tol=1e-4)
    return Ridge(solver="svd", alpha=1.0)


def worker(estimator_name, backend, dtype):
    torch.set_num_threads(4)
    n_samples, n_features = CASES[estimator_name]
    X_float32, y_np = make_data(estimator_name, n_samples, n_features)
    X, y = convert_data(X_float32, y_np, backend, dtype)
    del X_float32
    _trim_allocator()

    process = psutil.Process()
    baseline_rss = process.memory_info().rss
    splitter = (
        KFold(3, shuffle=True, random_state=0)
        if estimator_name == "Ridge"
        else StratifiedKFold(3, shuffle=True, random_state=0)
    )
    fit_times = []
    predict_times = []
    scores = []
    fitted_bytes = []

    with PeakRSS() as memory, threadpool_limits(limits=4):
        for train, test in splitter.split(np.empty(n_samples), y_np):
            X_train, X_test = take_rows(X, train), take_rows(X, test)
            y_train = take_rows(y, train)
            estimator = make_estimator(estimator_name)
            with config_context(array_api_dispatch=True):
                start = time.perf_counter()
                estimator.fit(X_train, y_train)
                fit_times.append(time.perf_counter() - start)

                start = time.perf_counter()
                prediction = estimator.predict(X_test)
                predict_times.append(time.perf_counter() - start)

            prediction = as_numpy(prediction)
            score = (
                r2_score(y_np[test], prediction)
                if estimator_name == "Ridge"
                else accuracy_score(y_np[test], prediction)
            )
            scores.append(score)
            fitted_bytes.append(model_nbytes(estimator))

    result = {
        "estimator": estimator_name,
        "backend": backend,
        "dtype": dtype,
        "n_samples": n_samples,
        "n_features": n_features,
        "input_mb": nbytes(X) / 2**20,
        "fit_s": float(np.sum(fit_times)),
        "predict_s": float(np.sum(predict_times)),
        "score_mean": float(np.mean(scores)),
        "score_std": float(np.std(scores)),
        "model_kb": float(np.mean(fitted_bytes) / 2**10),
        "rss_baseline_mb": baseline_rss / 2**20,
        "cv_peak_delta_mb": (memory.peak - baseline_rss) / 2**20,
    }
    print(json.dumps(result))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--estimator", choices=CASES)
    parser.add_argument("--backend", choices=("numpy", "torch"))
    parser.add_argument("--dtype", choices=("float32", "bfloat16"))
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("experiments/bfloat16_array_api/results/results.json"),
    )
    args = parser.parse_args()

    if args.worker:
        worker(args.estimator, args.backend, args.dtype)
        return

    results = []
    for estimator_name in CASES:
        for backend in ("numpy", "torch"):
            for dtype in ("float32", "bfloat16"):
                command = [
                    sys.executable,
                    __file__,
                    "--worker",
                    "--estimator",
                    estimator_name,
                    "--backend",
                    backend,
                    "--dtype",
                    dtype,
                ]
                completed = subprocess.run(
                    command, check=True, text=True, capture_output=True
                )
                results.append(json.loads(completed.stdout.splitlines()[-1]))
                print(completed.stdout.splitlines()[-1], flush=True)

    payload = {
        "metadata": {
            "platform": platform.platform(),
            "processor": platform.processor(),
            "python": platform.python_version(),
            "sklearn": sklearn.__version__,
            "numpy": np.__version__,
            "ml_dtypes": ml_dtypes.__version__,
            "torch": torch.__version__,
            "threads": 4,
            "cv_folds": 3,
        },
        "results": results,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n")


if __name__ == "__main__":
    main()
