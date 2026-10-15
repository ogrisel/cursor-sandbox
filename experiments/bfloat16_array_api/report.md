# Bfloat16 inputs for Array API estimators

## Conclusion

The three best candidates from scikit-learn main are `LogisticRegression`,
`GaussianNB`, and `Ridge`. Bfloat16 input storage is useful, but native bfloat16
solver state is not: preserving float32 accumulation keeps predictive quality
while halving the input arrays.

On this CPU, the practical win is memory rather than execution time.
`LogisticRegression` and `GaussianNB` reduce absolute peak process RSS by 29%
and 14–15%, respectively. `Ridge` does not reduce peak RSS because its float32
SVD workspace dominates. Fit and prediction are generally slower because of
the conversion to float32. These results do not justify promising a general
speedup from bfloat16 inputs.

## Inventory reviewed

The estimator list in `doc/modules/array_api.rst` on scikit-learn main contains:

| Family | Estimators |
| --- | --- |
| Covariance | `LedoitWolf`, `OAS` |
| Decomposition | `PCA` |
| Kernel approximation | `Nystroem` |
| Linear models | `LogisticRegression`, `LogisticRegressionCV`, `PoissonRegressor`, `Ridge`, `RidgeCV`, `RidgeClassifier`, `RidgeClassifierCV` |
| Discriminant analysis | `LinearDiscriminantAnalysis` |
| Naive Bayes | `GaussianNB` |
| Preprocessing | `Binarizer`, `KernelCenterer`, `LabelBinarizer`, `LabelEncoder`, `MaxAbsScaler`, `MinMaxScaler`, `Normalizer`, `PolynomialFeatures`, `StandardScaler` |
| Mixtures | `GaussianMixture` |

Meta-estimators were excluded because their benefit is inherited from a base
estimator. Preprocessors were excluded because the question asks about fit and
predict. `PCA`, `LinearDiscriminantAnalysis`, covariance estimators, and
`GaussianMixture` were deprioritized because their SVD, eigendecomposition, or
Cholesky kernels do not have robust native bfloat16 support in the tested
backends. The three selected estimators cover repeated matrix-vector products,
an SVD-based linear solve, and bandwidth-bound reductions.

## Implementation

- NumPy arrays backed by `ml_dtypes.bfloat16` are recognized as numeric and
  finite-checkable despite NumPy exposing their dtype kind as `V`.
- `LogisticRegression` and `Ridge` promote bfloat16 input to float32 rather than
  the previous accidental float64 conversion. Prediction aligns bfloat16 input
  with the fitted float32 coefficients.
- `GaussianNB` promotes before computing means and variances. The first
  iteration tried native bfloat16 statistics and accuracy fell from 0.9950 to
  0.6255; float32 accumulation restores accuracy to 0.9950.
- No runtime dependency on `ml_dtypes`, PyTorch, or CuPy is introduced.

## Cross-validation results

Each row is a three-fold CV total. Classification uses accuracy and Ridge uses
R². Peak RSS is the maximum resident set size of an isolated worker, including
the input array and CV workspaces. The host is a four-core x86-64 CPU with
AVX-512 BF16 and AMX BF16; no GPU was available.

### NumPy with ml_dtypes

| Estimator | Shape | dtype | Input MiB | Fit s | Predict s | Score | Peak RSS MiB |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| LogisticRegression | 400,000 × 256 | float32 | 390.6 | 0.623 | 0.071 | 0.892303 | 1,771.5 |
|  |  | bfloat16 | 195.3 | 0.794 | 0.121 | 0.892258 | 1,257.2 |
| GaussianNB | 800,000 × 128 | float32 | 390.6 | 2.011 | 0.708 | 0.994957 | 1,787.3 |
|  |  | bfloat16 | 195.3 | 2.997 | 1.159 | 0.994952 | 1,532.2 |
| Ridge | 30,000 × 512 | float32 | 58.6 | 2.246 | 0.011 | 0.999927 | 1,065.1 |
|  |  | bfloat16 | 29.3 | 2.113 | 0.023 | 0.999924 | 1,065.4 |

### PyTorch CPU

| Estimator | Shape | dtype | Input MiB | Fit s | Predict s | Score | Peak RSS MiB |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| LogisticRegression | 400,000 × 256 | float32 | 390.6 | 0.424 | 0.021 | 0.892303 | 1,783.7 |
|  |  | bfloat16 | 195.3 | 0.484 | 0.061 | 0.892258 | 1,272.9 |
| GaussianNB | 800,000 × 128 | float32 | 390.6 | 1.111 | 0.464 | 0.994957 | 1,801.5 |
|  |  | bfloat16 | 195.3 | 1.166 | 0.542 | 0.994955 | 1,539.5 |
| Ridge | 30,000 × 512 | float32 | 58.6 | 0.557 | 0.005 | 0.999927 | 867.1 |
|  |  | bfloat16 | 29.3 | 0.573 | 0.013 | 0.999924 | 864.4 |

## Interpretation

1. `LogisticRegression` is the strongest memory result. Peak RSS drops about
   29% on both backends and accuracy changes by only 0.000045. Fit is 14–27%
   slower and prediction is 71–182% slower, although prediction remains below
   0.13 seconds for all three folds.
2. `GaussianNB` drops peak RSS by 14–15% with effectively unchanged accuracy.
   PyTorch fit time rises only 5%; NumPy fit rises 49%. Stable float32 moments
   are essential.
3. `Ridge` halves stored input size and preserves R², but the float32 SVD
   workspace leaves peak RSS unchanged. NumPy fit is 6% faster in this single
   run while PyTorch fit is 3% slower; that is not enough evidence of a speed
   improvement.

The benchmark is CPU-only and each configuration was measured once. CuPy/CUDA
could change the trade-off, but common dense SVD implementations still promote
or reject bfloat16. Repeated runs and a CUDA host are needed before making a
backend-specific performance claim.

## Reproduce

```bash
export SCIPY_ARRAY_API=1
pixi run python experiments/bfloat16_array_api/benchmark.py
```

Raw measurements are in `results/results.json`.
