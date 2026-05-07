# HistGradientBoosting oversubscription diagnosis and mitigation

## Root-cause hypothesis

At high oversubscription (e.g. 16 OpenMP workers on a 4-core machine), `sklearn` HistGradientBoosting spends a large share of time in OpenMP scheduler / synchronization behavior instead of histogram work. This is consistent with:

- native profiles dominated by wait/sync frames (`clock_nanosleep`, pthread signaling / lock contention),
- large drops in speedup when threads exceed physical cores,
- much stronger sensitivity than XGBoost, which keeps histogram kernels dominant at 16 threads.

## Extra confirmation experiments

### 1) OMP wait-policy sensitivity at 16 threads

`OMP_WAIT_POLICY=PASSIVE` does **not** fix the issue (it is slower for sklearn and xgboost in this run, and only marginally better for lightgbm):

- `sklearn_hgb`: 3.105s -> 3.691s
- `xgboost_hist`: 2.330s -> 2.421s
- `lightgbm_hist`: 3.438s -> 3.396s

This rules out simple wait-policy tuning as a robust mitigation.

### 2) Context-switch instrumentation

Large-dataset means (3 repeats):

- `sklearn_hgb` @4 threads: ~49 voluntary context switches, fit ~1.704s.
- `sklearn_hgb` @16 threads: ~16,799 voluntary context switches, fit ~3.453s.
- `sklearn_hgb_fixed` @16 requested threads (capped to 4 effective): ~47 voluntary context switches, fit ~1.702s.

This directly supports an oversubscription-driven scheduling collapse in vanilla `sklearn_hgb`.

### 3) Early-stopping / tree-count parity check

All compared runs now explicitly check fitted tree counts from each library and enforce parity:

- expected trees from shared params: `n_estimators=160`
- fitted trees: sklearn=160, xgboost=160, lightgbm=160 (thread=1 and thread=16)
- fitted-tree spread across reference libraries at thread=1: `0.0`

So the observed runtime differences are not caused by unequal boosting lengths.

## Proposed simple sklearn code change

In `sklearn/ensemble/_hist_gradient_boosting/gradient_boosting.py`:

1. Add helper `_cap_threads_to_available_cpus(n_threads)` using `os.sched_getaffinity(0)` fallback `os.cpu_count()`.
2. Wrap all HistGB thread resolution calls:
   - fit-time `_openmp_effective_n_threads()`
   - predict-time `_openmp_effective_n_threads(n_threads)`
   - staged-predict thread resolution
   with the cap helper.

This keeps requested OpenMP worker count <= available CPUs for HistGB only.

## Validation summary

The benchmark harness includes `sklearn_hgb_fixed`, which emulates the above change by capping effective threads before fit/predict.

### Large dataset (`n_samples=176000`, `n_features=120`)

- `sklearn_hgb` speedup at 16 threads: **1.529x**
- `sklearn_hgb_fixed` speedup at 16 threads: **2.927x**
- R2 unchanged for sklearn original vs fixed.
- Cross-library aligned-R2 spread at thread=1 remains low (**0.000215**).
- Cross-library fitted-tree spread at thread=1 is **0.0**.

### Small dataset (`n_samples=60000`, `n_features=80`)

- `sklearn_hgb` speedup at 16 threads: **0.798x** (still a strong oversubscription regression)
- `sklearn_hgb_fixed` speedup at 16 threads: **2.413x**
- R2 unchanged for sklearn original vs fixed.
- Cross-library aligned-R2 spread at thread=1 remains low (**0.000717**).
- Cross-library fitted-tree spread at thread=1 is **0.0**.
