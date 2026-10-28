# 020 — balanced clusters and features, with device-resident cuML input

The previous five-task mix pairs a large number of clusters with very few
features, or a wide matrix with very few clusters. This iteration adds
`k256-d128`: 150,000 float32 Gaussian rows, 128 features, and 256 centers.
Its `n * k * d` is 4.92 billion, comparable to `k100-d32` (4.80 billion),
but both the centroid count and the feature width are substantial.

The task is calibrated against stock scikit-learn before the full run. One
greedy k-means++ fit with 12 Lloyd iterations takes 6.60 s, comfortably under
the 60 s worker limit. The full result set is
[results.json](results.json).

The benchmark driver now resolves its own Pixi interpreter rather than
assuming the checkout is at `~/kmeans_lloyd`. It also changes the cuML
contract: the timed region now starts only after the samples and the
shared-random-row centers are CuPy arrays on the NVIDIA L4. `output_type="cupy"`
keeps the fitted centers on the device, and their transfer for the
host-side inertia check happens after timing. This matches the existing
PyTorch and CuPy array-API paths. The relevant code is
[`_worker_cuml`](https://github.com/ogrisel/cursor-sandbox/blob/6cd77af81e4d1a11a9191cee85a149ac16413b61/kmeans_lloyd/scripts/bench_task_mix.py#L393-L430)
and [`_pythons`](https://github.com/ogrisel/cursor-sandbox/blob/6cd77af81e4d1a11a9191cee85a149ac16413b61/kmeans_lloyd/scripts/bench_task_mix.py#L81-L92).

## Setup

- One host: four CPU threads and one NVIDIA L4. Float32, TF32 disabled, three
  seeds, greedy k-means++ followed by at most 12 Lloyd iterations, and
  `tol=1e-8`.
- CPU contenders are stock scikit-learn 1.7.2 and cakedev0's scikit-learn
  1.10.dev0 build at
  [`7e26a5c`](https://github.com/cakedev0/scikit-learn/commit/7e26a5c37e1fa8031bef7da0ee43b633b07c8b9b).
  GPU contenders are eager array API on PyTorch CUDA and CuPy CUDA, plus cuML
  26.10.00.
- “Native” uses `index_add_` for PyTorch or `add.at` for CuPy. “Generic”
  forces the portable one-hot update. At `k=256, d=128`, both CUDA backends
  dispatch to the native update.
- The first CuPy-native and cuML process paid one-time initialization costs
  (10.2 s and 3.6 s). Their seed-0 cells were rerun with a warm cache and
  replace those values in `results.json`.

## Full fit from greedy k-means++

Time in seconds, mean ± sample standard deviation:

| hardware | implementation | k256-d128 |
| --- | --- | ---: |
| CPU | Torch array API, native | 5.808 ± 0.061 |
| CPU | Torch array API, generic | 6.610 ± 0.028 |
| CPU | scikit-learn 1.7.2 | 6.609 ± 0.023 |
| CPU | cakedev0 PRs 23+26 | **1.660 ± 0.015** |
| GPU | Torch array API, native | 0.491 ± 0.000 |
| GPU | Torch array API, generic | 0.510 ± 0.002 |
| GPU | CuPy array API, native | **0.478 ± 0.004** |
| GPU | CuPy array API, generic | 0.504 ± 0.001 |
| GPU | cuML greedy | 0.510 ± 0.023 |
| GPU | cuML scalable | **0.242 ± 0.002** |

- Native updates improve full fits by 1.14× on Torch CPU, 1.04× on Torch
  CUDA, and 1.05× on CuPy. The CPU gain is meaningful because the update is
  a larger fraction of this balanced task; on GPU, assignment and
  initialization dominate.
- Cakedev0 is 3.50× faster than native Torch CPU. The array-API CPU path
  nevertheless beats stock scikit-learn by 1.14×.
- With training data already device-resident for every GPU contender, native
  CuPy is 1.07× faster than cuML greedy. cuML scalable is 1.98× faster than
  native CuPy, but reaches a worse objective (below).

## Lloyd from the same random rows

This removes initializer cost and uses the same saved random data rows as
centers for every contender.

| hardware | implementation | k256-d128 |
| --- | --- | ---: |
| CPU | Torch array API, native | 2.031 ± 0.032 |
| CPU | Torch array API, generic | 2.774 ± 0.026 |
| CPU | scikit-learn 1.7.2 | **0.501 ± 0.000** |
| CPU | cakedev0 PRs 23+26 | **0.501 ± 0.002** |
| GPU | Torch array API, native | 0.218 ± 0.001 |
| GPU | Torch array API, generic | 0.233 ± 0.001 |
| GPU | CuPy array API, native | 0.189 ± 0.001 |
| GPU | CuPy array API, generic | 0.212 ± 0.001 |
| GPU | cuML | **0.120 ± 0.001** |

- Native over generic is 1.37× on Torch CPU, 1.07× on Torch CUDA, and 1.12×
  on CuPy.
- Cakedev0 does not change the shared-start Lloyd time: it ties stock
  scikit-learn at 0.501 s. Its full-fit advantage is therefore its
  k-means++ implementation.
- cuML is 1.58× faster than the fastest array-API Lloyd implementation
  (native CuPy) when both receive device-resident training data.

## Quality and memory

All greedy full fits end between 118.919 and 118.930 inertia per point. The
shared-start values agree within 0.0005, around 118.960. cuML scalable is
faster but finishes at 119.708: 0.66% above the best greedy result. This is
consistent with the large-`k` scalable-initializer behavior in
[011](../011-consolidated-benchmark/report.md).

The input occupies about 73 MiB. Every array-API full fit peaks around
147 MiB above its allocator baseline; stock scikit-learn and cakedev0 peak
around 146 MiB above `VmHWM`. The cuML `nvidia-smi` increments are 14 MiB for
greedy and 12 MiB for scalable. These meters are not directly comparable
across host and device allocators, but the cuML figures exclude the
pre-existing device input by construction.

## Conclusion

`k256-d128` fills the missing balanced region without threatening the
time limit. It confirms that native accumulation helps on CPU and remains a
small GPU win, while distinguishing the k-means++ advantage of cakedev0 from
its Lloyd kernel. It also changes the cuML comparison to a device-to-device
one: cuML is the fastest shared-start Lloyd kernel here, CuPy narrowly wins
against cuML greedy for the complete greedy fit, and cuML scalable is fastest
overall at a 0.66% objective cost.

Previous: [CPU and GPU optimization rerun](../019-cpu-gpu-optimization-rerun/report.md).
Index: [journal](../index.md).
