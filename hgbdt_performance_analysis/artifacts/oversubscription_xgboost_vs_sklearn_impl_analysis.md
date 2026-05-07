# Oversubscription analysis: why XGBoost degrades less than sklearn

## Scope

This note documents implementation-level explanations for:

1. Why XGBoost is more resilient to oversubscription than sklearn HistGradientBoosting and LightGBM on this benchmark.
2. Why sklearn (pre-fix) suffers the largest oversubscription slowdown.
3. What implementation changes in sklearn could reduce this issue without relying only on thread capping.

## Why XGBoost degrades less in oversubscription

### 1) Thread count is normalized centrally before core kernels run

XGBoost resolves thread count through `Context::Threads()`, which calls `common::OmpGetNumThreads(nthread)` and then applies cgroup-aware clamping:

- `src/context.cc`:
  - `Context::Threads()` returns `min(OmpGetNumThreads(...), cfs_cpu_count_)` when cgroup quotas are available.
- `src/common/threading_utils.cc`:
  - `OmpGetNumThreads()` clamps against OpenMP/runtime limits and returns 1 when already in an OpenMP parallel region.

This centralized policy reduces accidental over-requesting and nested parallelism overhead.

### 2) Work is organized as coarse blocked spaces (better scheduling granularity)

XGBoost histogram and split evaluation use `BlockedSpace2d` + `ParallelFor2d`:

- `src/common/threading_utils.h`: `BlockedSpace2d`, `ParallelFor2d`.
- `src/tree/hist/histogram.h`: histogram construction over blocked `(node, range)` workspaces.
- `src/tree/hist/evaluate_splits.h`: split search over blocked `(node, feature-subrange)` workspaces.

This increases useful work per scheduling event, which tends to be more robust under oversubscription than many tiny parallel regions.

### 3) Thread-local histogram accumulation + explicit reductions

XGBoost allocates per-thread partial histograms and merges them explicitly:

- `src/common/hist_util.h`: `ParallelGHistBuilder` (`GetInitializedHist`, `ReduceHist`, thread/node mapping).

This design reduces fine-grained contention on shared histogram updates.

### 4) Multi-node processing in one parallel stage

In split evaluation, XGBoost processes a set of candidate nodes together and reduces thread-local best splits:

- `src/tree/hist/evaluate_splits.h`: `EvaluateSplits(...)` allocates `tloc_candidates[n_threads * entries]` and reduces once.

Maintaining broader parallel regions with larger task batches generally degrades less when thread count exceeds physical cores.

## Why sklearn (pre-fix) suffers most

### 1) Before the mitigation, HistGB paths did not cap to available CPUs

Pre-fix code paths relied on `_openmp_effective_n_threads(...)` directly in fit/predict/staged-predict for HistGB, without an affinity-based cap:

- See patch artifact `artifacts/sklearn_histgb_thread_cap.patch` for the exact call sites changed in
  `sklearn/ensemble/_hist_gradient_boosting/gradient_boosting.py`.

### 2) Best-first growth induces many small parallel phases

sklearn grower processes one best node at a time (`heappop`), repeatedly invoking:

- split partitioning (`split_indices`)
- histogram build for smallest child (`compute_histograms_brute`)
- split search (`find_node_split`)

Paths:

- `sklearn/ensemble/_hist_gradient_boosting/grower.py`

As nodes get smaller, fixed high thread counts amplify scheduling overhead relative to useful work.

### 3) Several hotspots use fixed-thread `prange` even for small work units

Examples:

- histogram build:
  - `histogram.pyx`: `prange(..., num_threads=n_threads)` for sample reorder and feature hist loops.
- split partition:
  - `splitting.pyx`: two `prange(n_threads)` passes + offsets + `memcpy` merge in `split_indices`.
- split search:
  - `splitting.pyx`: `prange` over allowed features per node in `find_node_split`.

With oversubscription, many such short regions increase barrier/scheduler cost.

### 4) Runtime evidence aligns with scheduler-thrash interpretation

From benchmark artifacts:

- `artifacts/oversubscription_fix_validation.md`:
  - sklearn at 16 requested threads shows very large voluntary context switch counts and speedup collapse.
  - fixed variant (effective threads reduced to available cores) restores context-switch profile and scalability.
- `artifacts/oversubscription_profile_summary.md`:
  - sklearn 16-thread native profile shifts toward wait/synchronization signatures relative to productive histogram frames.

## Can sklearn avoid this without simple global thread capping?

Yes. A cap is a robust safety net, but it is not the only viable fix. Implementation-level alternatives:

### A) Adaptive per-node thread selection (granularity-aware)

Use a dynamic `n_jobs_local` in hist/split/partition kernels based on estimated work:

- `n_samples_at_node`
- `n_allowed_features`
- `n_bins`

Example policy:

- tiny node: serial path
- medium node: few threads
- large node: full thread budget

This directly targets oversubscription inefficiency on small nodes.

### B) Batch multiple nodes in parallel stages

Refactor the grow loop to evaluate/build for multiple frontier nodes together (level-wise or mini-batched best-first), enabling larger blocked workspaces similar to XGBoost's `(node, feature-range)` parallelization.

### C) Specialize `split_indices` for small-node fast paths

`split_indices` currently pays two parallel passes and merge machinery. For small nodes, a serial or low-thread path can reduce synchronization and buffer-copy overhead.

### D) Reuse thread-local scratch buffers across node operations

Persist thread-local buffers across repeated split/hist calls to avoid per-node temporary setup/teardown costs in tight loops.

## Practical conclusion

The observed difference is not only "OpenMP is bad at oversubscription": it is strongly tied to how each implementation shapes parallel work.

- XGBoost keeps coarser blocked tasks, thread-local accumulation, and centralized thread governance.
- sklearn pre-fix combines high thread counts with many short node-level parallel phases, so scheduler overhead dominates sooner when oversubscribed.

Long-term, adaptive granularity and batched-node execution are the most promising sklearn-internal fixes beyond hard thread caps.

## Recheck after enforcing equal fitted tree counts

The benchmark harness now explicitly records and validates fitted tree counts for every run (sklearn `n_iter_`, xgboost `num_boosted_rounds()`, lightgbm `current_iteration()`), and enforces equality with requested `n_estimators`.

The oversubscription conclusions above still hold after this check:

- reference-library fitted-tree spread at thread=1 is 0
- sklearn still shows the strongest oversubscription slowdown without mitigation
- the scheduler-overhead signature (context switch inflation) remains consistent with prior analysis
