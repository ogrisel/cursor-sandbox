# xsimd extension benchmark

| kernel | threading | threads | median (ms) | vs tabmat | max rel err | notes |
|---|---|---:|---:|---:|---:|---|
| tabmat | single | 1 | 2.09 | 1.00x | 0.00e+00 | reference native xsimd in tabmat |
| xsimd_ext | single | 1 | 33.24 | 0.06x | 1.66e-12 | xsimd batch width=8 |
| tabmat | multi | 4 | 6.85 | 1.00x | 0.00e+00 | reference native xsimd in tabmat |
| xsimd_ext | multi | 4 | 7.52 | 0.91x | 9.00e-13 | xsimd batch width=8 |
