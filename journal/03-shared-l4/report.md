# Shared NVIDIA L4

## Setup

The GPU benchmark uses PyTorch 2.14.1+cu130 on an NVIDIA L4 (23,034 MiB, compute capability 8.9). The host has 15 GiB of RAM and was shared with other agents. The checkout lived in `/tmp/cursor-bfloat16-f5d4`.

Values below are medians of three isolated workers; each worker runs three CV folds. The script waits for three consecutive idle samples (utilization at most 10% and at least 8,000 MiB free), rejects runs with competing GPU processes at fold boundaries, and requires at least 20% conservative free headroom. No final run was rejected, minimum free memory was 14,093 MiB, and timing coefficients of variation were at most 1.1%. Eighteen workers were accepted.

`GaussianNB` could not be scaled to a fit longer than one second without giving up that headroom. A smaller calibration used the CPU shapes and is kept as [gpu_smoke.json](gpu_smoke.json). The scaled measurements are in [gpu_results.json](gpu_results.json).

## Results

| Estimator | Shape | dtype | Input MiB | Fit s | Predict s | Score | Peak allocated MiB |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| LogisticRegression | 3,600,000 × 256 | float32 | 3,515.6 | 0.873 | 0.037 | 0.891849 | 7,180.7 |
|  |  | bfloat16 | 1,757.8 | 0.906 | 0.060 | 0.891840 | 6,008.7 |
| GaussianNB | 6,400,000 × 128 | float32 | 3,125.0 | 0.285 | 0.238 | 0.994948 | 8,470.3 |
|  |  | bfloat16 | 1,562.5 | 0.320 | 0.220 | 0.994949 | 7,427.6 |
| Ridge | 300,000 × 512 | float32 | 585.9 | 0.860 | 0.010 | 0.999914 | 2,944.5 |
|  |  | bfloat16 | 293.0 | 0.867 | 0.013 | 0.999911 | 2,748.5 |

## Interpretation

1. `LogisticRegression` saves 1,172 MiB (16%) of peak allocated memory. Fit is 4% slower and prediction is 63% slower because both paths compute in float32 after accepting bfloat16 storage.
2. `GaussianNB` saves 1,043 MiB (12%). Fit is 12% slower, while prediction is 7% faster. Accuracy differs by approximately one part per million.
3. `Ridge` saves 196 MiB (7%). Fit is 1% slower and prediction is 35% slower; the float32 SVD workspace still dominates.

The absence of broad speedups is expected. Tensor Cores on the L4 are not used, because fit and predict cast bfloat16 storage to float32 before the numeric kernels. `LogisticRegression` and single-target `Ridge` prediction are matrix-vector products, Ridge's SVD stays in float32, and `GaussianNB` is reductions and elementwise arithmetic. A later speedup would need float32 fitting followed by bfloat16 coefficients on a large GEMM, such as multiclass or multi-output prediction, or a PCA transform. That needs its own accuracy and API design.

CPU measurements and the ten-candidate ranking are in the [CPU report](../02-cpu-float32/report.md). The native-statistics failure that motivated float32 accumulation is [iteration 1](../01-native-gnb/report.md).

## Reproduce

Install this environment, then install scikit-learn from branch `cursor/bfloat16-array-api-experimental-f5d4` once that branch is on `github.com/ogrisel/scikit-learn`. Until the push is possible, the same sources are in sandbox commit `3242a51`. CuPy was not measured.

```bash
export SCIPY_ARRAY_API=1
pixi run python experiments/bfloat16_array_api/benchmark.py
pixi run python experiments/bfloat16_array_api/gpu_benchmark.py
```

Return to the [journal](../index.md).
