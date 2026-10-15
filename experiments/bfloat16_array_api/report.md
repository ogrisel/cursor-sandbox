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

Repeated NVIDIA L4 runs reach the same conclusion. Bfloat16 reduces peak
allocated GPU memory by 16% for `LogisticRegression`, 12% for `GaussianNB`, and
7% for `Ridge`. Scores are unchanged at the reported precision. Only
`GaussianNB.predict` is faster (7%); fit is 1–12% slower for all three.

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

## Top 10 candidates

This ranking includes inference-like `transform` workloads for transformers.
The first three have implemented support and are benchmarked below; the
remaining seven are recommendations for follow-up work.

| Rank | Estimator | Most promising bfloat16 phase | Main constraint |
| ---: | --- | --- | --- |
| 1 | `LogisticRegression` | Large-batch fit and linear prediction | L-BFGS/Newton state must remain float32 |
| 2 | `Ridge` | Design-matrix storage and prediction GEMM | SVD does not robustly support bfloat16 |
| 3 | `GaussianNB` | Bandwidth-bound fit and prediction | Means and variances require float32 accumulation |
| 4 | `PCA` | Transform GEMM and randomized range finding | SVD/eigendecomposition and whitening are precision-sensitive |
| 5 | `PolynomialFeatures` | Expansion of wide, dense inputs | High-degree products quickly lose mantissa precision |
| 6 | `PoissonRegressor` | Repeated loss/gradient matrix products | Optimizer state and exponential link need float32 |
| 7 | `Nystroem` | Pairwise kernel construction and transform | Distance calculations and normalization often upcast |
| 8 | `GaussianMixture` | Repeated E-step scoring on large batches | Cholesky and covariance updates need float32 |
| 9 | `LinearDiscriminantAnalysis` | Linear prediction and projection | Both SVD stages are precision-sensitive |
| 10 | `StandardScaler` | Memory-bound transform | Variance accumulation must remain float32 |

`LogisticRegressionCV`, `RidgeClassifier`, and the Ridge CV/classifier variants
inherit the same opportunities as their underlying algorithm and are not given
separate ranks.

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

## CPU cross-validation results

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

## CPU interpretation

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

## NVIDIA L4 results

The GPU benchmark uses PyTorch 2.14.1+cu130 on an NVIDIA L4. Values are medians
of three isolated workers; each worker runs three CV folds. The script waits
for three consecutive idle samples, requires at least 8,000 MiB free before
starting, rejects runs with competing GPU processes at fold boundaries, and
requires at least 20% conservative free headroom. No final run was rejected,
minimum free memory was 14,093 MiB, and timing coefficients of variation were
at most 1.1%.

| Estimator | Shape | dtype | Input MiB | Fit s | Predict s | Score | Peak allocated MiB |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| LogisticRegression | 3,600,000 × 256 | float32 | 3,515.6 | 0.873 | 0.037 | 0.891849 | 7,180.7 |
|  |  | bfloat16 | 1,757.8 | 0.906 | 0.060 | 0.891840 | 6,008.7 |
| GaussianNB | 6,400,000 × 128 | float32 | 3,125.0 | 0.285 | 0.238 | 0.994948 | 8,470.3 |
|  |  | bfloat16 | 1,562.5 | 0.320 | 0.220 | 0.994949 | 7,427.6 |
| Ridge | 300,000 × 512 | float32 | 585.9 | 0.860 | 0.010 | 0.999914 | 2,944.5 |
|  |  | bfloat16 | 293.0 | 0.867 | 0.013 | 0.999911 | 2,748.5 |

`GaussianNB` is so bandwidth-efficient that even the largest workload
compatible with generous shared-host headroom remains below one second.
Increasing it enough to cross that threshold would consume most of the L4 and
would violate the shared-resource policy.

## GPU interpretation

1. `LogisticRegression` saves 1,172 MiB (16%) of peak allocated memory. Fit is
   4% slower and prediction is 63% slower because both paths compute in
   float32 after accepting bfloat16 storage.
2. `GaussianNB` saves 1,043 MiB (12%). Fit is 12% slower, while prediction is
   7% faster. Accuracy differs by approximately one part per million.
3. `Ridge` saves 196 MiB (7%). Fit is 1% slower and prediction is 35% slower;
   the float32 SVD workspace still dominates.

The absence of broad speedups is expected: this implementation intentionally
uses float32 for numerically sensitive solver state. A future prediction-only
mode that stores linear coefficients in bfloat16 could exercise Tensor Cores,
but it needs a separate accuracy and API-compatibility design.

## Reproduce

```bash
export SCIPY_ARRAY_API=1
pixi run python experiments/bfloat16_array_api/benchmark.py
pixi run python experiments/bfloat16_array_api/gpu_benchmark.py
```

Raw measurements are in `results/results.json` and
`results/gpu_results.json`.
