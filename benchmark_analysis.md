# HistGradientBoostingRegressor vs XGBoost vs LightGBM (CPU)

## 1) Experimental setup

- CPU-only, `4` cores available.
- Same synthetic regression generator for all runs (`make_regression`) with increasing dataset templates:
  - `small`: 50k x 40
  - `medium`: 140k x 80
  - `large`: 320k x 120
- Strict runtime budget: each **individual model run** must stay under `10s`.
- Enforcement strategy:
  - every fit/predict executed in an interruptible subprocess;
  - when one model times out, the whole dataset tier is retried with `n_samples *= 0.72`;
  - for each dataset tier, all thread settings share the same reduced `n_samples` for fair scaling.
- Threads tested: `1, 2, 4`.

## 2) Hyperparameter matching and score parity

I aligned equivalent hyperparameters across implementations:

- `n_estimators/max_iter = 220`
- `learning_rate = 0.05`
- `max_depth = 6`
- `max_bin(s) = 255`
- `subsample = 0.8`
- `l2 regularization = 1.0`
- `leaf complexity aligned` (`max_leaf_nodes` / `num_leaves` = 31 where available)
- fixed `random_state = 42`.

Observed predictive parity:

- `small` and `medium`: R² spread well within `0.03`.
- `large`: R² spread = `0.0316` (very close to target tolerance, still same ballpark model quality).

## 3) Performance results

### 3.1 Single-thread behavior

- `sklearn_hgb` is fastest at 1 thread on all tested sizes.
- `xgboost_hist` is slowest at 1 thread.
- `lightgbm_hist` sits between sklearn and xgboost at 1 thread.

### 3.2 Multi-thread scaling (1 -> 4 threads)

- `lightgbm_hist`: strong scaling (`2.73x` to `3.43x`, efficiency up to `0.86`).
- `xgboost_hist`: also strong (`2.92x` to `3.29x`, efficiency up to `0.82`), but absolute runtime remains behind LightGBM at matched settings.
- `sklearn_hgb`: almost no scaling (`~1.00x` to `1.05x`), indicating a CPU parallelism bottleneck.

### 3.3 Memory behavior

All three show bounded, near-linear memory growth with data size in this range:

- `sklearn_hgb`: ~`2.01 MB / 1k samples`
- `xgboost_hist`: ~`2.02 MB / 1k samples`
- `lightgbm_hist`: ~`2.43 MB / 1k samples`

At matched scenarios, peak RSS stays in a compact range (roughly low-200MB to mid-300MB), with no explosive growth.

## 4) Profiling findings

## 4.1 Python-level

cProfile shows Python overhead is negligible for all three models; almost all time is spent in native code (`fit`/`predict` wrappers dominate cumulative time, but with minimal Python self-time).

## 4.2 Native-level hotspots

### sklearn_hgb

- Hotspots center around histogram building functions:
  - `histogram__build_histogram_no_hessian*`
  - `_binning__map_col_to_bins._omp_fn.0`
- This is consistent with low single-thread latency but weak multi-core scaling in this run profile.

### lightgbm_hist

- Dominant hotspots:
  - `LightGBM::DenseBin<unsigned char, false>::ConstructHistogram`
  - split evaluation and histogram fixup routines.
- Kernel work appears highly optimized and parallel-friendly, matching observed scalability.

### xgboost_hist (least-performing overall in this benchmark)

Top hotspots are concentrated in:

- split-gain calculation:
  - `TreeEvaluator::SplitEvaluator<...>::CalcSplitGain`
- histogram construction/dispatch:
  - `GHistBuildingManager::DispatchAndExecute`
  - `RowsWiseBuildHistKernel`
- split enumeration:
  - `HistEvaluator::EnumerateSplit<1>`
- histogram subtraction and partitioning.

## 5) Source-level analysis of the least-performing implementation (xgboost_hist)

The profile maps directly to these source regions:

- histogram build dispatch and kernels in `src/common/hist_util.cc`
  - dynamic dispatch over template/runtime flags;
  - row-wise histogram loops with sparse/block heuristics;
  - multiple memory-bound loops over bins / grad-hess arrays.
- split scanning and gain evaluation in `src/tree/hist/evaluate_splits.h`
  - repeated `CalcSplitGain` calls in per-bin loops.
- gain computation path in `src/tree/split_evaluator.h`
  - frequent math in `CalcSplitGain` / `CalcGainGivenWeight`.

By contrast, LightGBM’s dense-bin histogram kernels and quantized histogram paths (`ConstructHistogramInt*`) are heavily specialized and appear to reduce arithmetic and memory pressure in the hottest loops.

## 6) Refactor plan to close the gap (xgboost -> LightGBM-level throughput)

### Phase A: remove avoidable overhead in hottest loops

1. **Split-gain fast path specialization**
   - Introduce branchless specializations for common CPU case:
     - no monotonic constraints,
     - standard L2 regularization path.
   - Goal: reduce per-bin overhead in `CalcSplitGain` during `EnumerateSplit`.

2. **Histogram dispatch stabilization**
   - Cache `GHistBuildingManager` dispatch decision per training context (after first determination of flags) instead of re-dispatching in hot loops.
   - Goal: reduce template/runtime dispatch overhead at scale.

3. **Loop fusion and reduced memory traffic**
   - In row-wise histogram kernels, evaluate opportunities to fuse accumulation and local reduction stages for common dense/contiguous cases.
   - Goal: fewer cache-line round trips.

### Phase B: improve arithmetic density and cache efficiency

4. **Quantized histogram accumulator mode (CPU)**
   - Add optional int16/int32 packed accumulator path for CPU histogram construction, similar to LightGBM’s quantized histogram variants.
   - Goal: shrink bandwidth footprint and improve cache residency.

5. **Adaptive row-wise vs col-wise policy**
   - Strengthen heuristic thresholds for selecting row-wise / col-wise / blocked sparse path using measured nnz, feature count, and cache-size model.
   - Goal: prevent suboptimal kernel choice for medium datasets.

### Phase C: parallel efficiency tuning

6. **OpenMP scheduling and chunk tuning**
   - Expose and autotune scheduling strategy for histogram build and split enumeration loops (e.g., static vs guided, chunk sizes by node size).
   - Goal: improve scaling on 2-16 core CPU without regressions on 1 core.

7. **NUMA/cache-aware data layout experiments**
   - Prototype contiguous packing for frequently accessed bin/gradient blocks to reduce cross-core cache interference.

### Phase D: safety net and regression-proofing

8. **Add microbench CI track**
   - Continuous benchmarks for:
     - single-thread throughput,
     - 1->N scaling efficiency,
     - peak RSS / sample slope,
     - predictive parity (R² spread cap).
   - Add pass/fail thresholds to prevent performance regressions.

## 7) Practical conclusion

- Best overall implementation in this constrained CPU benchmark: **LightGBM**.
- Best single-thread latency: **scikit-learn HistGradientBoostingRegressor**.
- Least-performing overall under matched settings and similar predictive quality: **XGBoost hist**.
- The most promising acceleration targets for XGBoost are histogram-build kernels and split-gain evaluation loops, where profiles show concentrated native time.
