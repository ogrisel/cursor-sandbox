# sklearn HistGradientBoostingRegressor vs LightGBM (aligned hyperparameters)

## Hyperparameter alignment used for fair comparison

Shared configuration (identical values passed to both libraries):

- `n_estimators=180`
- `learning_rate=0.05`
- `max_depth=4`
- `num_leaves=31`
- `max_bin=255`
- `subsample=1.0`
- `l2_regularization=3.0`
- `min_samples_leaf=30`
- `min_child_weight=30.0`
- `min_split_gain=0.0`
- fixed `random_state=42`

## Predictive parity check

On the focused datasets, score gaps are very small:

- `medium_plus` (140k x 80): `|R²_sklearn - R²_lightgbm| = 0.000597`
- `larger` (176k x 100): `|R²_sklearn - R²_lightgbm| = 0.000413`

This is tight enough to compare implementation efficiency directly.

## Single-thread and thread-scalability summary

### medium_plus (140k x 80)

- sklearn: `fit 3.706s (1T) -> 1.189s (4T)`, speedup `3.118x`, efficiency `0.779`
- lightgbm: `fit 4.483s (1T) -> 1.369s (4T)`, speedup `3.274x`, efficiency `0.818`

### larger (176k x 100)

- sklearn: `fit 5.468s (1T) -> 1.717s (4T)`, speedup `3.183x`, efficiency `0.796`
- lightgbm: `fit 6.922s (1T) -> 2.220s (4T)`, speedup `3.118x`, efficiency `0.780`

Observed pattern:

- sklearn has better 1-thread latency in these aligned runs.
- lightgbm shows slightly better scaling on medium size, while both are close on larger size.
- sklearn’s remaining scalability headroom appears as lower efficiency on the medium workload.

## Root-cause analysis from profile + source contrast

## 1) sklearn hotspot pattern indicates memory-bound scattered histogram updates

Top sklearn native hotspots:

- `histogram__build_histogram_no_hessian*`
- `histogram__build_histogram_root_no_hessian*`
- `_binning__map_col_to_bins._omp_fn.0`

The corresponding sklearn Cython code updates global histogram structs directly in tight loops:

- `_build_histogram_no_hessian` writes `out[feature_idx, bin]` per sample with no thread-local reduction buffer.
- root variant does the same on all samples.

This pattern is efficient at low thread count but tends to become memory-bandwidth/cache-pressure limited under higher parallelism.

## 2) LightGBM hotspot code uses more specialized histogram kernels

Top LightGBM hotspots:

- `LightGBM::DenseBin<unsigned char, false>::ConstructHistogram`
- `Dataset::ConstructHistogramsInner<...>`

Its source shows:

- explicit prefetch-friendly histogram loops in `DenseBin::ConstructHistogramInner`.
- optional packed integer histogram kernels (`ConstructHistogramInt*`) reducing accumulator footprint.
- organized per-group histogram construction in `Dataset::ConstructHistogramsInner`.

Compared with sklearn’s direct `hist_struct` updates, this design improves arithmetic density and cache behavior in the hottest path.

## 3) sklearn still spends meaningful time in bin mapping path

`_binning._map_col_to_bins` appears as a recurring sklearn hotspot; it performs per-feature binary-search binning with OpenMP over rows.

While parallelized, the binary-search + branch-heavy pattern can dilute scaling versus LightGBM’s histogram path that concentrates more work in compact dense-bin kernels after dataset construction.

## 4) Parallelization granularity differs

In sklearn histogram construction, `compute_histograms_brute` parallelizes over features (`prange` on features) and repeatedly builds per-feature histograms.

With moderate feature counts and smaller per-feature chunks deeper in trees, this can lead to less ideal parallel granularity than LightGBM’s dense-bin/grouped kernels on some dataset sizes.

## Practical conclusion

- With aligned parameters and matched R², sklearn is not globally slower here; it is faster at 1 thread and competitive at 4 threads.
- The residual suboptimal point for sklearn is **parallel efficiency on medium-size workload**, where LightGBM’s specialized dense-bin histogram kernels scale a bit better.
- The source/profile contrast points to the same cause: sklearn’s histogram+binning path is more memory/branch heavy, while LightGBM packs more work into cache-friendly specialized kernels.

