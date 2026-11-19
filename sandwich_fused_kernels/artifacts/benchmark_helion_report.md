# Helion / torch.compile benchmark

| kernel | threading | threads | median (ms) | vs tabmat | max rel err | notes |
|---|---|---:|---:|---:|---:|---|
| torch_einsum | single | 1 | 1.61 | n/a | 5.95e-16 | eager PyTorch |
| torch_compile_einsum | single | 1 | 3.08 | n/a | 5.95e-16 | torch.compile CPU inductor |
| torch_compile_weighted_gram | single | 1 | 1.06 | n/a | 5.95e-16 | torch.compile CPU inductor |
| helion_eager | single | 1 | 1.75 | n/a | 5.95e-16 | Helion ref_mode=EAGER (CPU reference tiles) |
| helion_triton | n/a | 0 | 0.00 | n/a | 0.00e+00 | skipped: no CUDA GPU in this environment |
