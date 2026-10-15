# Experiment journal

## 2026-10-15 — Candidate inventory

Reviewed the estimator inventory on scikit-learn main and selected
`LogisticRegression`, `GaussianNB`, and `Ridge`. The selection favors matrix
products and bandwidth-bound reductions while avoiding estimators whose primary
kernel is an unsupported bfloat16 eigendecomposition or Cholesky factorization.

## 2026-10-15 — Native bfloat16 statistics

The initial implementation kept `GaussianNB` statistics in bfloat16. It reduced
memory and allowed both PyTorch and NumPy/`ml_dtypes` execution, but variance
rounding destroyed predictive performance on the benchmark.

See [iteration 1](archive/iteration-01-native-gnb.md).

## 2026-10-15 — Float32 accumulation

All three candidates now accept bfloat16 storage but use float32 solver state
and prediction arithmetic. This keeps the input-memory benefit while recovering
predictive performance.

See the [final report](report.md) and
[raw results](results/results.json).

## 2026-10-15 — Shared NVIDIA L4

Prepared `/tmp/cursor-bfloat16-f5d4` on the remote host and waited through two
periods of 100% utilization by another process. A quick calibration established
stable timings, then three scaled repeats were collected only after three
consecutive idle samples. All accepted runs retained at least 14,093 MiB free
under the conservative peak estimate.

The GPU confirms a memory-only benefit for most workloads: peak allocations
fall 7–16%, scores remain stable, and only `GaussianNB.predict` becomes faster.

See the [GPU calibration](results/gpu_smoke.json),
[scaled GPU results](results/gpu_results.json), and
[final report](report.md).
