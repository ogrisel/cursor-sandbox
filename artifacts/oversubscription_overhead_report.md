# Oversubscription overhead investigation (1, 2, 4, 8, 16 threads on 4 cores)

## Observed speedup degradation

From the aligned scalability sweep (`n_samples=176000`, `n_features=120`):

- `sklearn_hgb`: speedup drops from `2.922x` at 4 threads to `1.098x` at 8 threads and `0.945x` at 16 threads (worse than 1-thread at 16).
- `lightgbm_hist`: speedup drops from `3.091x` at 4 threads to `1.923x` at 8 threads and `1.753x` at 16.
- `xgboost_hist`: mild degradation only, from `3.110x` at 4 threads to `2.843x` at 8 and `2.801x` at 16.

## Main overhead causes from 4-thread vs 16-thread profiles

### sklearn_hgb

- 16-thread profile is dominated by synchronization/runtime frames and waiting signatures (`clock_nanosleep`, `pthread_cond_signal`, unnamed OpenMP/runtime addresses), while histogram kernels lose relative dominance.
- Python profile also shows increased lock-acquire/join overhead in the 16-thread run.
- Interpretation: strong oversubscription contention and scheduling overhead on top of histogram/binning work.

### lightgbm_hist

- At 16 threads, waiting/scheduler signatures (`clock_nanosleep`) and dataset-construction/runtime helper frames become much more prominent relative to pure histogram work.
- Histogram kernels remain present, but thread-management overhead grows enough to cut speedup significantly beyond 4 threads.
- Interpretation: oversubscription shifts runtime from useful parallel histogram work to thread scheduling and contention.

### xgboost_hist

- Core histogram-build kernels remain dominant at 16 threads (`RowsWiseBuildHistKernel`, `GHistBuildingManager` dispatch path), with some additional wait/runtime overhead.
- Degradation is smaller than sklearn/lightgbm, indicating better tolerance to oversubscription in this workload, but still below the 4-thread optimum.

## Practical takeaway

- On this 4-core machine, all libraries are best at or near 4 threads.
- Oversubscription to 8/16 threads causes significant efficiency loss for sklearn and lightgbm, and moderate loss for xgboost.
