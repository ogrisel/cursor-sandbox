# Iteration 1: native GaussianNB bfloat16 statistics

The first implementation retained bfloat16 means and variances. On a synthetic
120,000 × 128 classification problem with three-fold cross-validation:

| Backend | dtype | Input MiB | Fit s | Predict s | Accuracy |
| --- | --- | ---: | ---: | ---: | ---: |
| NumPy | float32 | 58.6 | 0.164 | 0.059 | 0.9950 |
| NumPy + ml_dtypes | bfloat16 | 29.3 | 0.544 | 0.346 | 0.6255 |
| PyTorch CPU | float32 | 58.6 | 0.140 | 0.076 | 0.9950 |
| PyTorch CPU | bfloat16 | 29.3 | 0.155 | 0.034 | 0.9945 |

NumPy/`ml_dtypes` showed that direct low-precision variance accumulation is not
portable or numerically acceptable. The final implementation promotes
`GaussianNB` computation to float32, matching the policy used for the linear
estimators.

Return to the [journal](../journal.md).
