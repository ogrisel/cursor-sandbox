# Lloyd k-means, one iteration, and kernel fusion

Array-API implementation of a single Lloyd iteration, plus a CUDA experiment
on whether PyTorch Inductor (`torch.compile`) and CuPy (`cupy.fuse`) fuse
nearest-centroid `argmin` into the squared Euclidean distance.

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
python scripts/render_site.py
```

`NVIDIA_TF32_OVERRIDE=0` is set in the pixi environment so PyTorch and CuPy
both run IEEE float32 matmuls.

Results land in `journal/*/results.json`. The narrative is the journal.
`python scripts/render_site.py` builds `site/`.

For pull requests, CI publishes the rendered site to GitHub Pages under
`pr-<number>/`, displays the URL in the deployment summary, and maintains a
pull-request comment with the same URL.
