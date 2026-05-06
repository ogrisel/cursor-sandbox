# Shared hyperparameter calibration

| candidate | dataset | n_samples | n_features | r2_spread | r2_mean | max_total_s |
| --- | --- | --- | --- | --- | --- | --- |
| cfg_a_depth4_leaf15 | medium | 90000 | 80 | 0.001665 | 0.661560 | 3.7021 |
| cfg_a_depth4_leaf15 | large_like | 120000 | 100 | 0.000912 | 0.598357 | 5.9039 |
| cfg_b_depth5_leaf31 | medium | 90000 | 80 | 0.001806 | 0.737554 | 4.2941 |
| cfg_b_depth5_leaf31 | large_like | 120000 | 100 | 0.000521 | 0.678941 | 6.8941 |
| cfg_c_depth3_leaf8 | medium | 90000 | 80 | 0.000999 | 0.721273 | 3.3377 |
| cfg_c_depth3_leaf8 | large_like | 120000 | 100 | 0.001924 | 0.660144 | 5.4844 |
| cfg_d_depth4_leaf31_more_reg | medium | 90000 | 80 | 0.001157 | 0.636165 | 3.4293 |
| cfg_d_depth4_leaf31_more_reg | large_like | 120000 | 100 | 0.001410 | 0.572369 | 5.6724 |

Best candidate: `cfg_d_depth4_leaf31_more_reg`
