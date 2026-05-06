# HistGradientBoosting oversubscription diagnosis and mitigation

## Root-cause hypothesis

At high oversubscription (e.g. 16 OpenMP workers on a 4-core machine), `sklearn` HistGradientBoosting spends a large share of time in OpenMP scheduler / synchronization behavior instead of histogram work. This is consistent with:

- native profiles dominated by wait/sync frames (`clock_nanosleep`, pthread signaling / lock contention),
- large drops in speedup when threads exceed physical cores,
- much stronger sensitivity than XGBoost, which keeps histogram kernels dominant at 16 threads.

## Extra confirmation experiments

### 1) OMP wait-policy sensitivity at 16 threads

`OMP_WAIT_POLICY=PASSIVE` does **not** fix the issue (and is slower here for all libraries, including `sklearn_hgb`: 4.781s -> 5.944s with unchanged R2). This rules out simple busy-wait policy tuning as a robust mitigation.

### 2) Context-switch instrumentation

Large-dataset means (3 repeats):

- `sklearn_hgb` @4 threads: ~55 voluntary context switches, fit ~1.966s.
- `sklearn_hgb` @16 threads: ~50,412 voluntary context switches, fit ~6.550s.
- `sklearn_hgb_fixed` @16 requested threads (capped to 4 effective): ~55 voluntary context switches, fit ~2.038s.

This directly supports an oversubscription-driven scheduling collapse in vanilla `sklearn_hgb`.

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

- `sklearn_hgb` speedup at 16 threads: **1.031x**
- `sklearn_hgb_fixed` speedup at 16 threads: **2.975x**
- R2 unchanged for sklearn original vs fixed.
- Cross-library aligned-R2 spread at thread=1 remains low (**0.001098**).

### Small dataset (`n_samples=60000`, `n_features=80`)

- `sklearn_hgb` speedup at 16 threads: **0.700x** (catastrophic regression)
- `sklearn_hgb_fixed` speedup at 16 threads: **2.661x**
- R2 unchanged for sklearn original vs fixed.
- Cross-library aligned-R2 spread at thread=1 remains low (**0.001329**).
