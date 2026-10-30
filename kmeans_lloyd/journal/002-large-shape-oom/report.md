# Large shape, eager GEMM out of memory

The first scaling attempt used one sample-heavy problem that is too big for eager temporaries, then tried to continue. It is kept as its own iteration because the out-of-memory result is evidence about fusion, not a failed run to hide.

| | sample-heavy |
| --- | --- |
| samples | 524288 |
| centroids | 2048 |
| features | 4096 |
| `X` | 8 GiB |
| distance matrix `(n, k)` | 4 GiB |
| broadcast tensor `(n, k, d)` | 16 TiB |

Eager code was refused up front when the estimated temporary would leave under 20% of the 23 GiB card free. The 16 TiB broadcast is in that category. Eager GEMM was allowed through that check and then failed inside `X * X`, which is another full copy of the samples, before the 4 GiB GEMM output could be allocated. The driver reported 1.76 GiB free at the moment a 4 GiB allocation was requested.

`torch.compile` on the same GEMM argmin ran. Median time 0.90 s, peak extra 4.01 GiB, classified as a materialized distance matrix. That is the `(n, k)` GEMM output with the squared-norm terms and `argmin` folded into the epilogue, which is the same split the probe showed with kernel names. The 8 GiB `X * X` buffer is gone, so the call fits.

A running tile of 32 centroids on this same `X`:

| schedule | result |
| --- | --- |
| eager running tile | out of memory allocating another 8 GiB difference |
| `torch.compile` running tile | 0.209 s, peak extra 6.00 MiB |

6.00 MiB is exactly `n * 8 + n * 4` bytes: the int64 labels and the float32 winning distances, and nothing else. The compiler kept the 32-centroid argmin inside the distance kernel on a problem whose broadcast tensor is 256 GiB. Sixty-four such tiles would cover every centroid. One tile times 64 is about 13 s, so the full pass was not launched in this round.

After this case the process still reported only 5.7 GiB free, and the centroid-heavy and feature-heavy problems were skipped by the headroom check. `empty_cache` alone did not drop compiler reference cycles. The following iteration calls `gc.collect()` before releasing the pool, and uses three shapes whose eager `X * X` plus distance matrix fit with room to spare.

Previous: [fusion probe](../001-fusion-probe/report.md). Next: [three shapes that fit](../003-resized-shapes/report.md).
