### init: mean seconds

| method | k100-d32 | k550-d6 | k3000-d2 |
| --- | ---: | ---: | ---: |
| labels-only | 5.778 | 3.612 | 7.238 |
| augmented GEMM | 3.271 | 3.077 | 6.129 |

### lloyd: mean seconds

| method | k100-d32 | k550-d6 | k3000-d2 |
| --- | ---: | ---: | ---: |
| previous | 3.399 | 3.729 | 11.473 |
| labels-only | 2.978 | 3.696 | 11.052 |
| interleaved | 3.110 | 2.830 | 9.574 |
| augmented Lloyd | 2.336 | 2.502 | 4.631 |

### fit: mean seconds

| method | k100-d32 | k550-d6 | k3000-d2 |
| --- | ---: | ---: | ---: |
| previous | 8.056 | 6.882 | 18.921 |
| labels-only | 7.731 | 6.994 | 17.821 |
| augmented GEMM | 5.072 | 5.355 | 10.695 |
| augmented Lloyd | 7.501 | 5.739 | 11.629 |

### Historical cakedev0 gap and speedup projection

| phase | task | old array API / cakedev0 | local speedup | projected optimized / cakedev0 |
| --- | --- | ---: | ---: | ---: |
| init | k100-d32 | 8.33x | 1.77x | 4.71x |
| init | k550-d6 | 7.04x | 1.17x | 6.00x |
| init | k3000-d2 | 7.17x | 1.18x | 6.07x |
| lloyd | k100-d32 | 6.42x | 1.46x | 4.41x |
| lloyd | k550-d6 | 3.37x | 1.49x | 2.26x |
| lloyd | k3000-d2 | 13.50x | 2.48x | 5.45x |
| fit | k100-d32 | 5.74x | 1.59x | 3.61x |
| fit | k550-d6 | 5.52x | 1.20x | 4.60x |
| fit | k3000-d2 | 8.86x | 1.63x | 5.44x |
