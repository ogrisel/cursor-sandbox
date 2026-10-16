# 008 — stochastic empty-center relocation and bounded task mix

This iteration adds an opt-in empty-center policy to the eager Python array-API implementation and evaluates a new bounded task mix.

## Empty-center policy

`reassign_empty=False` keeps the previous center, preserving the behavior in reports 001 through 007. With `reassign_empty=True`, the tiled update:

1. detects zero-count centers;
2. computes each sample's squared distance from its assigned old center;
3. draws distinct replacement samples with probability proportional to that squared error;
4. removes each selected sample from its donor sum and count; and
5. makes it the singleton member of the empty center before averaging.

Vanilla scikit-learn batch KMeans deterministically chooses the farthest samples. The array-API option uses a stochastic D² analogue, but it preserves scikit-learn's donor accounting rather than merely overwriting an empty center after the mean update. The random generator is explicit and the default remains disabled.

The CPU suite passes with 16 tests and 2 optional GPU skips. On the L4, the expanded suite passes all 20 tests, including this relocation on PyTorch CUDA and CuPy.

## Calibrated tasks

Data are standard Gaussian float32 matrices. Cluster and feature counts follow inverse, approximately logarithmic ranges so both requested endpoints fit in memory. Sample counts were calibrated against stock scikit-learn 1.7.2 with one k-means++ start, 12 iterations, and `tol=1e-8`.

| task | samples | clusters | features | calibration |
| --- | --- | --- | --- | --- |
| k3-d1000 | 950000 | 3 | 1000 | 11.65 s |
| k17-d180 | 2100000 | 17 | 180 | 10.40 s |
| k100-d32 | 1500000 | 100 | 32 | 12.92 s |
| k550-d6 | 525000 | 550 | 6 | 16.34 s |
| k3000-d2 | 135000 | 3000 | 2 | 29.56 s |

Each task uses seeds 0 through 2. The implementation-specific k-means++ track is separate from a paired random-start track: NumPy samples dataset rows once for each task and seed, and every Lloyd implementation receives exactly those rows. A no-Lloyd random-centroid baseline reports the quality of those same rows.

Contenders are eager array API with PyTorch CPU, PyTorch CUDA, and CuPy, each with relocation disabled and enabled; stock scikit-learn; scikit-learn with PRs 23 and 26; and cuML. Every worker is a fresh process with a hard 60-second wall timeout.

The 285-row matrix is in progress. This page will be replaced with aggregate plots, tables, timeout counts, and quality qualifications.
