# Portable array-API KMeans and kernel experiments

`kmeans_lloyd.KMeans` is a scikit-learn-compatible dense KMeans estimator
implemented with Python array API operations. It preserves NumPy, PyTorch, or
CuPy arrays on their original device and supports the public KMeans
hyperparameters that apply to dense Lloyd iterations. Initialization is
restricted to `"k-means++"` and `"random"`; sparse inputs and Elkan are
intentionally unsupported.

```python
from kmeans_lloyd import KMeans

model = KMeans(
    n_clusters=8,
    init="k-means++",
    n_init="auto",
    random_state=0,
).fit(X)

labels = model.labels_
centers = model.cluster_centers_
```

The package also contains lower-level Lloyd primitives and CUDA experiments
on assignment fusion and backend-specific centroid reductions.

The naive assignment is

```text
distances = sum((X[:, None, :] - centroids[None, :, :]) ** 2, axis=-1)
labels = argmin(distances, axis=1)
```

That broadcasts a difference tensor of shape `(n_samples, n_clusters, n_features)`.
The Gram form and the tiled / running schedules are rewrites used to give
the compilers a smaller region to fuse. Eager execution is always measured
beside the compiled or fused call.

## Reproduce

On a machine with an NVIDIA GPU whose driver supports CUDA 13:

```bash
cd kmeans_lloyd
pixi install
pixi run test
pixi run probe
pixi run bench
python ../tools/render_journal.py \
  --journal journal \
  --site site \
  --title "Lloyd k-means fusion journal"
```

`NVIDIA_TF32_OVERRIDE=0` is set in the pixi environment so PyTorch and CuPy
both run IEEE float32 matmuls.

Results land in `journal/*/results.json`. The narrative is the journal.
The shared renderer builds `site/`. Pull request CI calls
`.github/workflows/publish-report.yml`, which publishes that journal at
`pr-<number>/` and updates the pull request comment with the URL.
