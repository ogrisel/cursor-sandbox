# Bfloat16 Array API benchmarks

CPU and shared-GPU cross-validation for `LogisticRegression`, `Ridge`, and `GaussianNB` with bfloat16 inputs.

The scikit-learn changes are branch `cursor/bfloat16-array-api-experimental-f5d4` on [ogrisel/scikit-learn](https://github.com/ogrisel/scikit-learn), with no pull request. Published write-ups are in `journal/`.

```bash
export SCIPY_ARRAY_API=1
pixi run python experiments/bfloat16_array_api/benchmark.py
pixi run python experiments/bfloat16_array_api/gpu_benchmark.py
```
