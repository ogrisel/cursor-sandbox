### Torch CPU, init: seconds

| method | k3-d1000 | k17-d180 | k100-d32 | k550-d6 | k3000-d2 |
| --- | ---: | ---: | ---: | ---: | ---: |
| previous | 2.807 ± 0.006 | 4.203 ± 0.031 | 13.110 ± 0.245 | 14.083 ± 0.146 | 20.816 ± 0.244 |
| augmented init | 3.752 ± 0.005 | 4.074 ± 0.010 | 9.112 ± 0.019 | 11.351 ± 0.143 | 22.491 ± 0.167 |

### Torch CPU, lloyd: seconds

| method | k3-d1000 | k17-d180 | k100-d32 | k550-d6 | k3000-d2 |
| --- | ---: | ---: | ---: | ---: | ---: |
| previous | 16.494 ± 2.687 | 7.866 ± 0.074 | 5.471 ± 0.067 | 5.074 ± 0.014 | 20.787 ± 0.258 |
| labels-only | 14.198 ± 0.148 | 7.080 ± 0.068 | 4.882 ± 0.015 | 5.058 ± 0.010 | 20.760 ± 0.253 |
| interleaved | 13.689 ± 0.108 | 6.210 ± 0.012 | 5.156 ± 0.020 | 4.862 ± 0.001 | 19.921 ± 0.035 |
| augmented Lloyd | 15.734 ± 0.037 | 7.269 ± 0.085 | 4.186 ± 0.014 | 4.061 ± 0.009 | 6.608 ± 0.670 |

### Torch CPU, fit: seconds

| method | k3-d1000 | k17-d180 | k100-d32 | k550-d6 | k3000-d2 |
| --- | ---: | ---: | ---: | ---: | ---: |
| previous | 16.891 ± 0.264 | 11.400 ± 0.060 | 17.555 ± 0.402 | 18.374 ± 0.029 | 40.046 ± 0.462 |
| labels-only | 16.295 ± 0.021 | 10.618 ± 0.089 | 16.912 ± 0.070 | 18.345 ± 0.095 | 39.842 ± 0.139 |
| augmented init + Lloyd | 17.515 ± 0.134 | 10.338 ± 0.045 | 12.329 ± 0.099 | 14.577 ± 0.168 | 29.617 ± 0.081 |
| augmented Lloyd | 17.981 ± 0.172 | 10.873 ± 0.045 | 16.664 ± 0.317 | 17.479 ± 0.151 | 27.673 ± 0.179 |

### Torch CUDA, init: seconds

| method | k3-d1000 | k17-d180 | k100-d32 | k550-d6 | k3000-d2 |
| --- | ---: | ---: | ---: | ---: | ---: |
| previous | 0.106 ± 0.005 | 0.173 ± 0.000 | 0.332 ± 0.000 | 0.596 ± 0.003 | 1.368 ± 0.023 |
| augmented init | 0.137 ± 0.000 | 0.170 ± 0.000 | 0.202 ± 0.001 | 0.383 ± 0.002 | 1.325 ± 0.024 |

### Torch CUDA, lloyd: seconds

| method | k3-d1000 | k17-d180 | k100-d32 | k550-d6 | k3000-d2 |
| --- | ---: | ---: | ---: | ---: | ---: |
| previous | 0.635 ± 0.000 | 0.472 ± 0.008 | 0.244 ± 0.001 | 0.297 ± 0.001 | 0.430 ± 0.022 |
| labels-only | 0.626 ± 0.000 | 0.447 ± 0.006 | 0.224 ± 0.002 | 0.315 ± 0.000 | 0.434 ± 0.001 |
| interleaved | 0.609 ± 0.000 | 0.509 ± 0.013 | 0.261 ± 0.002 | 0.342 ± 0.001 | 0.480 ± 0.002 |
| augmented Lloyd | 0.663 ± 0.000 | 0.461 ± 0.006 | 0.178 ± 0.002 | 0.165 ± 0.003 | 0.256 ± 0.003 |

### Torch CUDA, fit: seconds

| method | k3-d1000 | k17-d180 | k100-d32 | k550-d6 | k3000-d2 |
| --- | ---: | ---: | ---: | ---: | ---: |
| previous | 0.738 ± 0.000 | 0.638 ± 0.004 | 0.577 ± 0.001 | 0.869 ± 0.003 | 1.759 ± 0.028 |
| labels-only | 0.729 ± 0.000 | 0.617 ± 0.000 | 0.561 ± 0.001 | 0.890 ± 0.002 | 1.765 ± 0.027 |
| augmented init + Lloyd | 0.765 ± 0.000 | 0.611 ± 0.004 | 0.381 ± 0.002 | 0.541 ± 0.006 | 1.536 ± 0.030 |
| augmented Lloyd | 0.767 ± 0.000 | 0.629 ± 0.009 | 0.514 ± 0.001 | 0.746 ± 0.007 | 1.578 ± 0.015 |

### CuPy CUDA, init: seconds

| method | k3-d1000 | k17-d180 | k100-d32 | k550-d6 | k3000-d2 |
| --- | ---: | ---: | ---: | ---: | ---: |
| previous | 0.102 ± 0.000 | 0.240 ± 0.000 | 0.694 ± 0.001 | 1.342 ± 0.002 | 2.869 ± 0.026 |
| augmented init | 0.142 ± 0.005 | 0.247 ± 0.000 | 0.565 ± 0.001 | 1.148 ± 0.001 | 2.906 ± 0.026 |

### CuPy CUDA, lloyd: seconds

| method | k3-d1000 | k17-d180 | k100-d32 | k550-d6 | k3000-d2 |
| --- | ---: | ---: | ---: | ---: | ---: |
| previous | 0.814 ± 0.000 | 0.551 ± 0.003 | 0.305 ± 0.003 | 0.329 ± 0.001 | 0.478 ± 0.030 |
| labels-only | 0.806 ± 0.000 | 0.490 ± 0.005 | 0.291 ± 0.002 | 0.330 ± 0.001 | 0.460 ± 0.003 |
| interleaved | 0.792 ± 0.000 | 0.564 ± 0.006 | 0.346 ± 0.002 | 0.394 ± 0.007 | 0.553 ± 0.001 |
| augmented Lloyd | 0.843 ± 0.001 | 0.500 ± 0.003 | 0.245 ± 0.001 | 0.239 ± 0.003 | 0.406 ± 0.007 |

### CuPy CUDA, fit: seconds

| method | k3-d1000 | k17-d180 | k100-d32 | k550-d6 | k3000-d2 |
| --- | ---: | ---: | ---: | ---: | ---: |
| previous | 0.919 ± 0.001 | 0.794 ± 0.002 | 1.002 ± 0.005 | 1.657 ± 0.004 | 3.302 ± 0.017 |
| labels-only | 0.912 ± 0.001 | 0.729 ± 0.001 | 0.981 ± 0.003 | 1.664 ± 0.004 | 3.299 ± 0.030 |
| augmented init + Lloyd | 0.953 ± 0.001 | 0.728 ± 0.002 | 0.810 ± 0.000 | 1.402 ± 0.007 | 3.355 ± 0.020 |
| augmented Lloyd | 0.949 ± 0.001 | 0.740 ± 0.002 | 0.942 ± 0.001 | 1.576 ± 0.005 | 3.227 ± 0.037 |

### Speedup over the previous implementation

| row | k3-d1000 | k17-d180 | k100-d32 | k550-d6 | k3000-d2 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Torch CPU, init, augmented init | 0.75x | 1.03x | 1.44x | 1.24x | 0.93x |
| Torch CPU, lloyd, labels-only | 1.16x | 1.11x | 1.12x | 1.00x | 1.00x |
| Torch CPU, lloyd, interleaved | 1.20x | 1.27x | 1.06x | 1.04x | 1.04x |
| Torch CPU, lloyd, augmented Lloyd | 1.05x | 1.08x | 1.31x | 1.25x | 3.15x |
| Torch CPU, fit, labels-only | 1.04x | 1.07x | 1.04x | 1.00x | 1.01x |
| Torch CPU, fit, augmented init + Lloyd | 0.96x | 1.10x | 1.42x | 1.26x | 1.35x |
| Torch CPU, fit, augmented Lloyd | 0.94x | 1.05x | 1.05x | 1.05x | 1.45x |
| Torch CUDA, init, augmented init | 0.78x | 1.02x | 1.65x | 1.55x | 1.03x |
| Torch CUDA, lloyd, labels-only | 1.01x | 1.06x | 1.09x | 0.94x | 0.99x |
| Torch CUDA, lloyd, interleaved | 1.04x | 0.93x | 0.93x | 0.87x | 0.90x |
| Torch CUDA, lloyd, augmented Lloyd | 0.96x | 1.03x | 1.37x | 1.79x | 1.68x |
| Torch CUDA, fit, labels-only | 1.01x | 1.03x | 1.03x | 0.98x | 1.00x |
| Torch CUDA, fit, augmented init + Lloyd | 0.96x | 1.04x | 1.52x | 1.61x | 1.14x |
| Torch CUDA, fit, augmented Lloyd | 0.96x | 1.01x | 1.12x | 1.16x | 1.11x |
| CuPy CUDA, init, augmented init | 0.71x | 0.97x | 1.23x | 1.17x | 0.99x |
| CuPy CUDA, lloyd, labels-only | 1.01x | 1.12x | 1.05x | 1.00x | 1.04x |
| CuPy CUDA, lloyd, interleaved | 1.03x | 0.98x | 0.88x | 0.84x | 0.87x |
| CuPy CUDA, lloyd, augmented Lloyd | 0.97x | 1.10x | 1.25x | 1.38x | 1.18x |
| CuPy CUDA, fit, labels-only | 1.01x | 1.09x | 1.02x | 1.00x | 1.00x |
| CuPy CUDA, fit, augmented init + Lloyd | 0.96x | 1.09x | 1.24x | 1.18x | 0.98x |
| CuPy CUDA, fit, augmented Lloyd | 0.97x | 1.07x | 1.06x | 1.05x | 1.02x |

### Peak memory increment (MiB)

| row | k3-d1000 | k17-d180 | k100-d32 | k550-d6 | k3000-d2 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Torch CPU, init, previous | 1007 | 1517 | 295 | 222 | 119 |
| Torch CPU, init, augmented init | 3751 | 1658 | 392 | 158 | 96 |
| Torch CPU, lloyd, previous | 998 | 2120 | 436 | 98 | 92 |
| Torch CPU, lloyd, labels-only | 998 | 2120 | 435 | 95 | 91 |
| Torch CPU, lloyd, interleaved | 998 | 2120 | 435 | 94 | 108 |
| Torch CPU, lloyd, augmented Lloyd | 3779 | 2121 | 435 | 104 | 104 |
| Torch CPU, fit, previous | 1008 | 2139 | 449 | 222 | 120 |
| Torch CPU, fit, labels-only | 1007 | 2139 | 449 | 222 | 119 |
| Torch CPU, fit, augmented init + Lloyd | 4656 | 3606 | 651 | 159 | 106 |
| Torch CPU, fit, augmented Lloyd | 3786 | 2139 | 449 | 222 | 119 |
| Torch CUDA, init, previous | 939 | 1450 | 213 | 98 | 32 |
| Torch CUDA, init, augmented init | 3668 | 1562 | 303 | 66 | 18 |
| Torch CUDA, lloyd, previous | 928 | 2052 | 368 | 74 | 68 |
| Torch CUDA, lloyd, labels-only | 928 | 2052 | 368 | 74 | 68 |
| Torch CUDA, lloyd, interleaved | 928 | 2052 | 368 | 74 | 68 |
| Torch CUDA, lloyd, augmented Lloyd | 3690 | 2052 | 368 | 88 | 69 |
| Torch CUDA, fit, previous | 939 | 2051 | 368 | 98 | 68 |
| Torch CUDA, fit, labels-only | 939 | 2051 | 368 | 98 | 68 |
| Torch CUDA, fit, augmented init + Lloyd | 4560 | 3509 | 563 | 90 | 70 |
| Torch CUDA, fit, augmented Lloyd | 3691 | 2051 | 368 | 98 | 69 |
| CuPy CUDA, init, previous | 939 | 1450 | 212 | 98 | 31 |
| CuPy CUDA, init, augmented init | 3667 | 1562 | 303 | 66 | 18 |
| CuPy CUDA, lloyd, previous | 928 | 2051 | 366 | 74 | 68 |
| CuPy CUDA, lloyd, labels-only | 928 | 2051 | 366 | 74 | 68 |
| CuPy CUDA, lloyd, interleaved | 928 | 2051 | 366 | 74 | 68 |
| CuPy CUDA, lloyd, augmented Lloyd | 3689 | 2051 | 366 | 88 | 69 |
| CuPy CUDA, fit, previous | 939 | 2051 | 366 | 98 | 68 |
| CuPy CUDA, fit, labels-only | 939 | 2051 | 366 | 98 | 68 |
| CuPy CUDA, fit, augmented init + Lloyd | 4559 | 3509 | 561 | 90 | 70 |
| CuPy CUDA, fit, augmented Lloyd | 3689 | 2051 | 366 | 98 | 69 |

### Mean inertia change from previous

| row | k3-d1000 | k17-d180 | k100-d32 | k550-d6 | k3000-d2 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Torch CPU, init, augmented init | +0.000% | +0.000% | +0.000% | -0.014% | +0.373% |
| Torch CPU, lloyd, labels-only | +0.000% | +0.000% | +0.000% | +0.000% | +0.000% |
| Torch CPU, lloyd, interleaved | -0.000% | +0.000% | -0.000% | -0.000% | -0.004% |
| Torch CPU, lloyd, augmented Lloyd | +0.000% | +0.000% | +0.000% | -0.000% | +0.000% |
| Torch CPU, fit, labels-only | +0.000% | +0.000% | +0.000% | +0.000% | +0.000% |
| Torch CPU, fit, augmented init + Lloyd | +0.000% | +0.000% | +0.000% | -0.004% | -0.076% |
| Torch CPU, fit, augmented Lloyd | +0.000% | +0.000% | +0.000% | +0.000% | +0.000% |
| Torch CUDA, init, augmented init | -0.056% | +0.286% | +1.077% | -0.020% | -0.029% |
| Torch CUDA, lloyd, labels-only | +0.000% | -0.000% | -0.000% | -0.000% | +0.001% |
| Torch CUDA, lloyd, interleaved | +0.000% | +0.000% | -0.000% | -0.000% | +0.002% |
| Torch CUDA, lloyd, augmented Lloyd | +0.000% | -0.000% | -0.000% | -0.000% | -0.001% |
| Torch CUDA, fit, labels-only | +0.000% | +0.000% | -0.002% | -0.089% | +0.184% |
| Torch CUDA, fit, augmented init + Lloyd | +0.000% | +0.000% | +0.011% | -0.099% | -0.067% |
| Torch CUDA, fit, augmented Lloyd | +0.000% | +0.000% | -0.003% | -0.102% | +0.086% |
| CuPy CUDA, init, augmented init | +0.000% | -0.266% | +0.031% | +0.045% | +0.378% |
| CuPy CUDA, lloyd, labels-only | +0.000% | -0.000% | +0.000% | +0.000% | +0.004% |
| CuPy CUDA, lloyd, interleaved | +0.000% | +0.000% | -0.000% | -0.000% | +0.004% |
| CuPy CUDA, lloyd, augmented Lloyd | +0.000% | +0.000% | -0.000% | +0.000% | +0.002% |
| CuPy CUDA, fit, labels-only | +0.000% | -0.000% | +0.000% | -0.000% | +0.000% |
| CuPy CUDA, fit, augmented init + Lloyd | +0.000% | +0.000% | +0.003% | +0.053% | +0.125% |
| CuPy CUDA, fit, augmented Lloyd | +0.000% | +0.000% | +0.000% | -0.000% | -0.001% |

### Same-host comparison with cakedev0 (time / cakedev0 time)

| row | k3-d1000 | k17-d180 | k100-d32 | k550-d6 | k3000-d2 |
| --- | ---: | ---: | ---: | ---: | ---: |
| cakedev0 seconds, init | 1.237 | 1.928 | 1.494 | 1.919 | 2.994 |
| Torch CPU previous / cakedev0, init | 2.27x | 2.18x | 8.78x | 7.34x | 6.95x |
| Torch CPU augmented init / cakedev0, init | 3.03x | 2.11x | 6.10x | 5.91x | 7.51x |
| Torch CUDA previous / cakedev0, init | 0.09x | 0.09x | 0.22x | 0.31x | 0.46x |
| Torch CUDA augmented init / cakedev0, init | 0.11x | 0.09x | 0.14x | 0.20x | 0.44x |
| CuPy CUDA previous / cakedev0, init | 0.08x | 0.12x | 0.46x | 0.70x | 0.96x |
| CuPy CUDA augmented init / cakedev0, init | 0.11x | 0.13x | 0.38x | 0.60x | 0.97x |
| cakedev0 seconds, lloyd | 6.337 | 3.079 | 1.424 | 1.316 | 1.541 |
| Torch CPU previous / cakedev0, lloyd | 2.60x | 2.55x | 3.84x | 3.85x | 13.49x |
| Torch CPU augmented Lloyd / cakedev0, lloyd | 2.48x | 2.36x | 2.94x | 3.09x | 4.29x |
| Torch CUDA previous / cakedev0, lloyd | 0.10x | 0.15x | 0.17x | 0.23x | 0.28x |
| Torch CUDA augmented Lloyd / cakedev0, lloyd | 0.10x | 0.15x | 0.12x | 0.13x | 0.17x |
| CuPy CUDA previous / cakedev0, lloyd | 0.13x | 0.18x | 0.21x | 0.25x | 0.31x |
| CuPy CUDA augmented Lloyd / cakedev0, lloyd | 0.13x | 0.16x | 0.17x | 0.18x | 0.26x |
| cakedev0 seconds, fit | 7.309 | 4.985 | 2.861 | 3.203 | 4.508 |
| Torch CPU previous / cakedev0, fit | 2.31x | 2.29x | 6.14x | 5.74x | 8.88x |
| Torch CPU augmented init + Lloyd / cakedev0, fit | 2.40x | 2.07x | 4.31x | 4.55x | 6.57x |
| Torch CPU augmented Lloyd / cakedev0, fit | 2.46x | 2.18x | 5.82x | 5.46x | 6.14x |
| Torch CUDA previous / cakedev0, fit | 0.10x | 0.13x | 0.20x | 0.27x | 0.39x |
| Torch CUDA augmented init + Lloyd / cakedev0, fit | 0.10x | 0.12x | 0.13x | 0.17x | 0.34x |
| Torch CUDA augmented Lloyd / cakedev0, fit | 0.10x | 0.13x | 0.18x | 0.23x | 0.35x |
| CuPy CUDA previous / cakedev0, fit | 0.13x | 0.16x | 0.35x | 0.52x | 0.73x |
| CuPy CUDA augmented init + Lloyd / cakedev0, fit | 0.13x | 0.15x | 0.28x | 0.44x | 0.74x |
| CuPy CUDA augmented Lloyd / cakedev0, fit | 0.13x | 0.15x | 0.33x | 0.49x | 0.72x |
