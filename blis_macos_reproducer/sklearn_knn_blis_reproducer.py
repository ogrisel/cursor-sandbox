#!/usr/bin/env python
"""Run the sklearn KNN imputer tests that fail on macOS arm64 with conda-forge BLIS."""

from __future__ import annotations

import subprocess
import sys

# Subset of failures from scikit-learn macOS pylatest_conda_forge_arm (BLIS default).
_KNN_TESTS = (
    "sklearn.impute.tests.test_knn::test_knn_imputer_with_simple_example",
    "sklearn.impute.tests.test_knn::test_knn_imputer_weight_distance",
    "sklearn.impute.tests.test_knn::test_knn_imputer_distance_weighted_not_enough_neighbors",
)


def main() -> int:
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "-xvs",
        "--tb=short",
        *_KNN_TESTS,
    ]
    print("Running:", " ".join(cmd), flush=True)
    return subprocess.call(cmd)


if __name__ == "__main__":
    sys.exit(main())
