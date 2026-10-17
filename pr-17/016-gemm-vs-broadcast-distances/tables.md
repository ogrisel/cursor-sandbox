### init: duration

| backend and method | k3-d1000 | k17-d180 | k100-d32 | k550-d6 | k3000-d2 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Torch CPU, gemm | 2.97 ± 0.01 s | 4.36 ± 0.04 s | 13.34 ± 0.08 s | 14.41 ± 0.11 s | 21.57 ± 0.15 s |
| Torch CPU, broadcast | 15.93 ± 0.57 s | 53.22 ± 1.14 s | 64.83 ± 1.33 s | 46.41 ± 0.94 s | 52.98 ± 6.42 s |
| Torch CUDA, gemm | 0.17 ± 0.01 s | 0.24 ± 0.01 s | 0.40 ± 0.00 s | 0.65 ± 0.00 s | 1.43 ± 0.00 s |
| Torch CUDA, broadcast | 0.64 ± 0.01 s | 1.89 ± 0.00 s | 2.27 ± 0.01 s | 1.40 ± 0.00 s | 1.41 ± 0.02 s |
| CuPy CUDA, gemm | 0.12 ± 0.01 s | 0.25 ± 0.00 s | 0.70 ± 0.00 s | 1.35 ± 0.00 s | 2.92 ± 0.03 s |
| CuPy CUDA, broadcast | 0.76 ± 0.35 s | 1.91 ± 0.00 s | 2.50 ± 0.01 s | 2.08 ± 0.00 s | 2.68 ± 0.03 s |

### init: broadcast / GEMM duration

| backend | k3-d1000 | k17-d180 | k100-d32 | k550-d6 | k3000-d2 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Torch CPU | 5.37x | 12.20x | 4.86x | 3.22x | 2.46x |
| Torch CUDA | 3.76x | 7.80x | 5.70x | 2.14x | 0.98x |
| CuPy CUDA | 6.56x | 7.65x | 3.57x | 1.55x | 0.92x |

### init: peak memory

| backend and method | k3-d1000 | k17-d180 | k100-d32 | k550-d6 | k3000-d2 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Torch CPU, gemm | 1007 MiB | 1518 MiB | 296 MiB | 223 MiB | 120 MiB |
| Torch CPU, broadcast | 1007 MiB | 1518 MiB | 436 MiB | 350 MiB | 119 MiB |
| Torch CUDA, gemm | 939 MiB | 1450 MiB | 213 MiB | 98 MiB | 32 MiB |
| Torch CUDA, broadcast | 939 MiB | 1450 MiB | 369 MiB | 258 MiB | 42 MiB |
| CuPy CUDA, gemm | 939 MiB | 1450 MiB | 212 MiB | 98 MiB | 31 MiB |
| CuPy CUDA, broadcast | 939 MiB | 1450 MiB | 369 MiB | 258 MiB | 42 MiB |

### init: broadcast / GEMM peak memory

| backend | k3-d1000 | k17-d180 | k100-d32 | k550-d6 | k3000-d2 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Torch CPU | 1.00x | 1.00x | 1.47x | 1.57x | 0.99x |
| Torch CUDA | 1.00x | 1.00x | 1.73x | 2.63x | 1.31x |
| CuPy CUDA | 1.00x | 1.00x | 1.74x | 2.63x | 1.33x |

### init: quality

| backend and method | k3-d1000 | k17-d180 | k100-d32 | k550-d6 | k3000-d2 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Torch CPU, gemm | 1910.83 | 291.777 | 31.5133 | 1.0865 | 0.0214486 |
| Torch CPU, broadcast | 1900.7 | 291.777 | 31.5856 | 1.08674 | 0.0214998 |
| Torch CUDA, gemm | 1912.09 | 293.169 | 31.6434 | 1.08629 | 0.0214833 |
| Torch CUDA, broadcast | 1911.01 | 292.765 | 31.4173 | 1.08724 | 0.021496 |
| CuPy CUDA, gemm | 1910.83 | 294.115 | 31.4811 | 1.08576 | 0.0214359 |
| CuPy CUDA, broadcast | 1910.83 | 293.333 | 31.5027 | 1.08616 | 0.0215041 |

### init: broadcast / GEMM quality

| backend | k3-d1000 | k17-d180 | k100-d32 | k550-d6 | k3000-d2 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Torch CPU | 0.994702x | 1.000000x | 1.002295x | 1.000223x | 1.002391x |
| Torch CUDA | 0.999438x | 0.998619x | 0.992857x | 1.000882x | 1.000591x |
| CuPy CUDA | 1.000000x | 0.997343x | 1.000685x | 1.000371x | 1.003178x |

### lloyd: duration

| backend and method | k3-d1000 | k17-d180 | k100-d32 | k550-d6 | k3000-d2 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Torch CPU, gemm | 15.11 ± 0.12 s | 8.25 ± 0.05 s | 5.68 ± 0.03 s | 5.25 ± 0.03 s | 21.94 ± 0.10 s |
| Torch CPU, broadcast | 90.06 ± 4.65 s | 189.96 ± 6.83 s | 142.99 ± 5.62 s | 71.77 ± 2.66 s | 51.32 ± 0.07 s |
| Torch CUDA, gemm | 0.78 ± 0.03 s | 0.54 ± 0.01 s | 0.29 ± 0.00 s | 0.37 ± 0.00 s | 0.51 ± 0.03 s |
| Torch CUDA, broadcast | 3.36 ± 0.00 s | 6.25 ± 0.01 s | 4.64 ± 0.01 s | 1.75 ± 0.00 s | 1.01 ± 0.00 s |
| CuPy CUDA, gemm | 0.93 ± 0.05 s | 0.60 ± 0.01 s | 0.32 ± 0.00 s | 0.37 ± 0.01 s | 0.54 ± 0.04 s |
| CuPy CUDA, broadcast | 3.45 ± 0.00 s | 6.36 ± 0.00 s | 4.54 ± 0.00 s | 1.79 ± 0.00 s | 1.01 ± 0.00 s |

### lloyd: broadcast / GEMM duration

| backend | k3-d1000 | k17-d180 | k100-d32 | k550-d6 | k3000-d2 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Torch CPU | 5.96x | 23.01x | 25.18x | 13.67x | 2.34x |
| Torch CUDA | 4.28x | 11.64x | 16.22x | 4.67x | 1.96x |
| CuPy CUDA | 3.73x | 10.56x | 14.01x | 4.83x | 1.87x |

### lloyd: peak memory

| backend and method | k3-d1000 | k17-d180 | k100-d32 | k550-d6 | k3000-d2 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Torch CPU, gemm | 998 MiB | 2121 MiB | 436 MiB | 99 MiB | 92 MiB |
| Torch CPU, broadcast | 998 MiB | 2121 MiB | 436 MiB | 138 MiB | 98 MiB |
| Torch CUDA, gemm | 928 MiB | 2052 MiB | 368 MiB | 74 MiB | 68 MiB |
| Torch CUDA, broadcast | 928 MiB | 2052 MiB | 368 MiB | 287 MiB | 164 MiB |
| CuPy CUDA, gemm | 928 MiB | 2051 MiB | 366 MiB | 74 MiB | 68 MiB |
| CuPy CUDA, broadcast | 928 MiB | 2051 MiB | 366 MiB | 286 MiB | 164 MiB |

### lloyd: broadcast / GEMM peak memory

| backend | k3-d1000 | k17-d180 | k100-d32 | k550-d6 | k3000-d2 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Torch CPU | 1.00x | 1.00x | 1.00x | 1.40x | 1.06x |
| Torch CUDA | 1.00x | 1.00x | 1.00x | 3.90x | 2.42x |
| CuPy CUDA | 1.00x | 1.00x | 1.00x | 3.89x | 2.42x |

### lloyd: quality

| backend and method | k3-d1000 | k17-d180 | k100-d32 | k550-d6 | k3000-d2 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Torch CPU, gemm | 998.868 | 176.534 | 25.9169 | 1.02721 | 0.0248171 |
| Torch CPU, broadcast | 998.868 | 176.534 | 25.9168 | 1.0272 | 0.0248656 |
| Torch CUDA, gemm | 998.868 | 176.534 | 25.9169 | 1.02721 | 0.0248157 |
| Torch CUDA, broadcast | 998.868 | 176.534 | 25.9169 | 1.02721 | 0.0248658 |
| CuPy CUDA, gemm | 998.868 | 176.534 | 25.9169 | 1.02721 | 0.0248147 |
| CuPy CUDA, broadcast | 998.868 | 176.534 | 25.9169 | 1.02721 | 0.0248656 |

### lloyd: broadcast / GEMM quality

| backend | k3-d1000 | k17-d180 | k100-d32 | k550-d6 | k3000-d2 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Torch CPU | 1.000000x | 1.000000x | 1.000000x | 0.999997x | 1.001953x |
| Torch CUDA | 1.000000x | 1.000000x | 1.000000x | 0.999998x | 1.002019x |
| CuPy CUDA | 1.000000x | 1.000000x | 1.000000x | 0.999996x | 1.002049x |

### fit: duration

| backend and method | k3-d1000 | k17-d180 | k100-d32 | k550-d6 | k3000-d2 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Torch CPU, gemm | 17.33 ± 0.20 s | 11.56 ± 0.08 s | 17.89 ± 0.33 s | 18.72 ± 0.20 s | 41.81 ± 0.42 s |
| Torch CPU, broadcast | 106.30 ± 0.90 s | 233.77 ± 5.53 s | 208.75 ± 9.94 s | 117.36 ± 1.24 s | 74.09 ± 5.67 s |
| Torch CUDA, gemm | 0.92 ± 0.00 s | 0.75 ± 0.00 s | 0.67 ± 0.00 s | 1.01 ± 0.00 s | 1.87 ± 0.02 s |
| Torch CUDA, broadcast | 3.99 ± 0.02 s | 8.13 ± 0.01 s | 6.89 ± 0.01 s | 3.14 ± 0.01 s | 2.36 ± 0.01 s |
| CuPy CUDA, gemm | 1.01 ± 0.00 s | 0.84 ± 0.00 s | 1.02 ± 0.00 s | 1.71 ± 0.01 s | 3.42 ± 0.01 s |
| CuPy CUDA, broadcast | 4.01 ± 0.01 s | 8.27 ± 0.00 s | 7.03 ± 0.01 s | 3.88 ± 0.01 s | 3.63 ± 0.05 s |

### fit: broadcast / GEMM duration

| backend | k3-d1000 | k17-d180 | k100-d32 | k550-d6 | k3000-d2 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Torch CPU | 6.14x | 20.22x | 11.67x | 6.27x | 1.77x |
| Torch CUDA | 4.32x | 10.79x | 10.24x | 3.11x | 1.26x |
| CuPy CUDA | 3.96x | 9.85x | 6.88x | 2.27x | 1.06x |

### fit: peak memory

| backend and method | k3-d1000 | k17-d180 | k100-d32 | k550-d6 | k3000-d2 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Torch CPU, gemm | 1009 MiB | 2140 MiB | 450 MiB | 223 MiB | 120 MiB |
| Torch CPU, broadcast | 1025 MiB | 2138 MiB | 444 MiB | 350 MiB | 120 MiB |
| Torch CUDA, gemm | 939 MiB | 2051 MiB | 368 MiB | 98 MiB | 68 MiB |
| Torch CUDA, broadcast | 939 MiB | 2051 MiB | 369 MiB | 286 MiB | 164 MiB |
| CuPy CUDA, gemm | 939 MiB | 2051 MiB | 366 MiB | 98 MiB | 68 MiB |
| CuPy CUDA, broadcast | 939 MiB | 2051 MiB | 369 MiB | 286 MiB | 164 MiB |

### fit: broadcast / GEMM peak memory

| backend | k3-d1000 | k17-d180 | k100-d32 | k550-d6 | k3000-d2 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Torch CPU | 1.02x | 1.00x | 0.99x | 1.57x | 0.99x |
| Torch CUDA | 1.00x | 1.00x | 1.00x | 2.92x | 2.42x |
| CuPy CUDA | 1.00x | 1.00x | 1.01x | 2.92x | 2.42x |

### fit: quality

| backend and method | k3-d1000 | k17-d180 | k100-d32 | k550-d6 | k3000-d2 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Torch CPU, gemm | 998.867 | 176.533 | 25.9156 | 1.02505 | 0.0181267 |
| Torch CPU, broadcast | 998.867 | 176.533 | 25.9151 | 1.02466 | 0.0181381 |
| Torch CUDA, gemm | 998.867 | 176.535 | 25.9159 | 1.02483 | 0.0181039 |
| Torch CUDA, broadcast | 998.867 | 176.534 | 25.9162 | 1.02489 | 0.0180876 |
| CuPy CUDA, gemm | 998.867 | 176.533 | 25.9167 | 1.02457 | 0.0180962 |
| CuPy CUDA, broadcast | 998.867 | 176.534 | 25.917 | 1.02487 | 0.0181368 |

### fit: broadcast / GEMM quality

| backend | k3-d1000 | k17-d180 | k100-d32 | k550-d6 | k3000-d2 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Torch CPU | 1.000000x | 1.000000x | 0.999982x | 0.999623x | 1.000626x |
| Torch CUDA | 1.000000x | 0.999996x | 1.000011x | 1.000057x | 0.999098x |
| CuPy CUDA | 1.000000x | 1.000002x | 1.000012x | 1.000291x | 1.002246x |
