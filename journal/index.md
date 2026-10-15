# Bfloat16 Array API journal

Bfloat16 input storage helps three Array API estimators, and float32 accumulation is required to keep their predictions intact. On CPU and on a shared NVIDIA L4, peak memory falls and predictive scores stay put. Fit does not get faster.

The estimator changes are the experimental branch `cursor/bfloat16-array-api-experimental-f5d4` on [ogrisel/scikit-learn](https://github.com/ogrisel/scikit-learn), based on main `d0e22aee7bbef7b310a2f08227c214ff6df9a526`. That branch has no pull request. This repository keeps the benchmarks and these reports.

## Cases

- [Native GaussianNB statistics](01-native-gnb/report.md)
- [Float32 accumulation on CPU](02-cpu-float32/report.md)
- [Shared NVIDIA L4](03-shared-l4/report.md)

## 2026-10-15 — Candidate inventory

Reviewed the estimator inventory on scikit-learn main and selected `LogisticRegression`, `GaussianNB`, and `Ridge`. The selection favors matrix products and bandwidth-bound reductions while avoiding estimators whose primary kernel is an unsupported bfloat16 eigendecomposition or Cholesky factorization.

The [CPU report](02-cpu-float32/report.md) expands the same review to ten candidates.

## 2026-10-15 — Native bfloat16 statistics

The initial implementation kept `GaussianNB` statistics in bfloat16. It reduced memory and allowed both PyTorch and NumPy/`ml_dtypes` execution, but variance rounding destroyed predictive performance on the benchmark.

See [iteration 1](01-native-gnb/report.md).

## 2026-10-15 — Float32 accumulation

All three candidates now accept bfloat16 storage but use float32 solver state and prediction arithmetic. This keeps the input-memory benefit while recovering predictive performance.

See the [CPU report](02-cpu-float32/report.md) and the [CPU measurements](02-cpu-float32/results.json).

## 2026-10-15 — Shared NVIDIA L4

Prepared `/tmp/cursor-bfloat16-f5d4` on the remote host and waited through two periods of 100% utilization by another process. A quick calibration established stable timings, then three scaled repeats were collected only after three consecutive idle samples. All accepted runs retained at least 14,093 MiB free under the conservative peak estimate.

The GPU confirms a memory-only benefit for most workloads: peak allocations fall 7–16%, scores remain stable, and only `GaussianNB.predict` becomes faster.

See the [L4 report](03-shared-l4/report.md), the [GPU calibration](03-shared-l4/gpu_smoke.json), and the [scaled GPU results](03-shared-l4/gpu_results.json).
