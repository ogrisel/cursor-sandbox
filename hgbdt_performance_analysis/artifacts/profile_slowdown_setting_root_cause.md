# Root-cause analysis for sklearn vs LightGBM slowdown (4 threads)

## Profiled setting

- Dataset: `n_samples=220000`, `n_features=8`, `threads=4`
- Hyperparameters: `n_estimators=12`, `learning_rate=0.14`, `max_depth=12`, `num_leaves=255`, `min_samples_leaf=20`, `min_child_weight=20.0`, `l2_regularization=10.0`, `max_bin=255`, `subsample=1.0`, `min_split_gain=0.1`

## Observed slowdown

- Mean fit time (12 repeats): sklearn `0.3516s` vs lightgbm `0.2137s`
- Relative slowdown: sklearn / lightgbm = `1.645x`

## Python-level profiler signal (single fit, cProfile)

- sklearn: `120,130` calls (`113,834` primitive), total `0.3539s`
- lightgbm: `4,206` calls (`3,772` primitive), total `0.1937s`
- Dominant sklearn path:
  - `gradient_boosting.py:fit` -> `grower.py:grow` -> `grower.py:split_next`
  - `split_next` is called `3,048` times in one fit and accounts for `0.2618s` cumulative time.
- Dominant lightgbm path:
  - `engine.py:train` -> `basic.py:update` (`12` calls, one per boosting round)
  - Most time is inside native update (`0.125s`) with far less Python orchestration.

## Native profiler signal (py-spy --native)

- Wait/synchronization share (samples where any frame matches wait/sync signatures):
  - sklearn: `53.17%`
  - lightgbm: `38.33%`
- sklearn native top leaves include:
  - `clock_nanosleep`, `pthread_cond_signal`, `split_indices._omp_fn.0`, `split_next`
- lightgbm native top leaves are mostly compute/data-kernel symbols:
  - `LGBM_DatasetCreateFromMats._omp_fn.0`, `DenseBin::Split`, `DenseBin::ConstructHistogram`
  - no wait/sleep symbol appears among top leaf frames.

## Root cause

The slowdown is primarily due to higher fine-grained control/synchronization overhead in sklearn's tree growth loop for this deep-leaf setting:

1. sklearn grows with a best-first loop (`while splittable_nodes: split_next()`), repeatedly splitting one node at a time and managing a heap.
2. Each split triggers node partitioning (`split_indices`) and split search (`find_node_split`), both using OpenMP-parallel regions for relatively small per-node tasks.
3. This results in many short synchronization phases, reflected by large wait/sleep sample share in native profiling.
4. LightGBM performs one native booster update per tree iteration in a tighter C++ path with lower Python dispatch overhead and a compute-heavier native profile.

Therefore, in this configuration (few trees, deep leaves), sklearn spends more time in repeated per-node orchestration and synchronization, while LightGBM keeps more work inside coarse native kernels.
