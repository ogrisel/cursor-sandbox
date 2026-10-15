# 007 — repeated seeds and shared fixed centers

The breadth comparison is being repeated with initializer seeds 0 through 4. Error bars will show one sample standard deviation across those five independent runs.

This iteration separates two questions:

1. How much do k-means++ basin selection, fit quality, duration, and memory vary with the random seed?
2. When every implementation receives exactly the same starting centers, how do the Lloyd implementations compare?

For the second question, NumPy selects `k` rows from each dataset without replacement for each seed. The selected float32 rows are saved once and passed unchanged to eager array-API PyTorch on CPU and CUDA, stock scikit-learn, scikit-learn with PRs 23 and 26, and cuML. Each implementation runs both one Lloyd step and a full Lloyd-only fit from those centers. The full fit uses the same 12-iteration budget and variance-scaled tolerance as [006](../006-breadth/index.html).

The array-API entry point for this path is `fit_lloyd`. `fit_kmeans` now composes k-means++ with that same function, so the fixed-center and initialized tracks do not maintain separate iteration loops.

## Validation before the full run

The CPU test suite passes with 14 tests and one optional-GPU skip. A five-backend smoke run on `tight`, seed 0, produced the same fixed-center quality within float32 accumulation noise:

| phase | API CPU | sklearn 1.7 | sklearn PRs | API CUDA | cuML |
| --- | --- | --- | --- | --- | --- |
| after one shared-center step | 277.56446 | 277.56443 | 277.56445 | 277.56438 | 277.56449 |
| after the shared-center fit | 248.89027 | 248.89024 | 248.89024 | 248.89030 | 248.89027 |

That particular random-row start is deliberately not presented as a good initializer: it misses blobs and all implementations spend the 12-iteration budget in the same poorer basin. It is useful precisely because it confirms that, after removing initializer differences, the five Lloyd paths agree on the resulting objective.

Progress checkpoint: 1,566 of 1,700 rows have completed with no worker failures. The first `speed-l` repetitions already confirm why the seed sweep matters: seed 3 puts the array-API fit on the separated-blob floor at mean inertia 1,023 after 2 iterations, whereas seed 0 in [006](../006-breadth/index.html) ended at 1,199. The remaining `speed-l` rows and all of `speed-xl` are still running. This page will be replaced with the plots, aggregate tables, and quality disclaimers when the run finishes.
