# Iterative HistGradientBoostingRegressor optimization report (main-based)

## Goal

Improve `sklearn.ensemble.HistGradientBoostingRegressor` performance to be competitive with the best benchmarked library across baseline and deep/few-tree settings.

## Method

1. Cloned `scikit-learn` from `main` into `scikit-learn-local/`.
2. Used `scikit-learn==1.9.dev0` nightly wheel for runnable binaries.
3. Iteratively edited main-branch Python sources in the local fork and synced changed files into the installed wheel for benchmark execution.
4. Re-ran the full harness each iteration with machine-scoped artifacts:
   - `linux-amd64-iter0` (baseline)
   - `linux-amd64-iter1` (cap + adaptive node-level thread gating)
   - `linux-amd64-iter2` (cap-only final retained patch)

## Iterations

### Iteration 0 (baseline)
- Stock nightly `sklearn` (main-dev).
- Severe oversubscription regressions remained (`t8`, `t16`), with worst sklearn/best ratio > `6x`.

### Iteration 1 (rejected)
- Added CPU-thread cap and adaptive per-node thread gating.
- Oversubscription improved, but regular-thread throughput (`t2`, `t4`) regressed significantly.
- Rejected this variant.

### Iteration 2 (retained)
- Kept only CPU-thread capping in HistGB fit/predict paths.
- Final patch: `artifacts/sklearn_main_iterative_patch_v1.diff`.

## Quantitative outcome (sklearn_hgb total runtime ratio vs best model in same setting)

| setting | iter0 median ratio | iter0 max ratio | iter2 median ratio | iter2 max ratio |
| --- | ---: | ---: | ---: | ---: |
| baseline_default | 1.182x | 6.339x | 1.064x | 1.177x |
| deep_few_trees | 1.243x | 6.267x | 1.042x | 1.423x |

Interpretation:
- Oversubscription collapse was eliminated in retained iteration (`max` dropped from `~6x` to `<= 1.423x`).
- Most scenarios became near-parity (`~1.04x - 1.08x` typical), with one remaining notable gap in deep/small at 4 threads.

## Remaining gap

- Worst remaining case in iter2 is deep setting, small dataset, `t4`, where sklearn is `1.423x` slower than the best model (LightGBM).
- This indicates the oversubscription issue is fixed, while deeper orchestration/kernel-efficiency differences remain in one regular-thread scenario.
