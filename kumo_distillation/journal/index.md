# Distilling Kumo-Tabular into HistGradientBoosting quantile models

Electricity load forecasting benchmark of
[probabl-ai/skore-example-electricity-load](https://github.com/probabl-ai/skore-example-electricity-load)
(walk-forward CV with forecast weather, 8 folds of 13 weeks, horizons 1h /
12h / 24h). The question: can a family of scikit-learn
`HistGradientBoostingRegressor` models, distilled from Kumo-Tabular with the
CutMix recipe of [arXiv:2610.01435](https://arxiv.org/html/2610.01435),
close the gap between `hgb_quantile_q7` and `kumo_tabular`? And does
post-hoc calibration help on top?

## Conclusion

Distillation does not close the gap. The paper recipe (squared-error students
on the teacher's 7 quantiles, [CutMix][cutmix] at a 2:1 synthetic-to-real
ratio, no ground-truth labels, in [`training_set`][training-set] and
[`fit_predict`][fit-predict]) moves average MAE from 859 MW to 847 MW,
against 686 MW for the teacher. Two properties of this forecasting setup
break the recipe: the teacher memorizes the training rows it sees as context
([`gen_teacher.py`][gen-teacher] predicts each training row with that row in
the context), and CutMix of two random hours falls off the data manifold.
Replacing the memorized targets with blocked out-of-fold teacher predictions
([`gen_teacher_oof.py`][gen-teacher-oof]) fixes the collapsed intervals and
makes the median worse.

The gain that does show up comes from the features, with no teacher involved.
[Differences of the load lags][lag-diffs], and a residual target relative to
the [last observed load][last-load], bring a label-trained HGB to 747 MW.
Leaving the median alone and shifting the other quantiles from the previous
4 folds ([`recalibrate`][recalibrate]) then puts its 90% coverage at 0.91
and its 7-level pinball loss at 232 MW, against 213 MW for the teacher.
Distilling on top of those same features is worse than training them on the
labels.

One combination was stopped before it finished: out-of-fold teacher targets
together with the lag-difference features (6 of 12 folds done). It is not in
the tables.

## Iterations

1. [Reproduction of `kumo_tabular` and `hgb_quantile_q7`](01-reproduction/report.md)
   on an AWS L4 GPU.
2. [Distillation into HGB students](02-distillation/report.md): the paper
   recipe, real rows only, out-of-fold targets, lag-difference features, and
   the teacher diagnostics.
3. [Post-hoc calibration](03-calibration/report.md) from the predictions of
   the 4 preceding walk-forward folds.

## Consolidated metrics

Pooled over the 8 evaluation folds. MAE and width in MW. "pinball q7" is the
mean pinball loss over the 7 levels and 3 horizons. Lower is better except
for d2 (higher is better) and coverage (target 0.90).

| model | MAE avg | MAE 1h | MAE 12h | MAE 24h | pinball q7 avg | d2 pinball avg | cov 90 avg | width 90 avg |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| hgb_quantile_q7 (upstream) | 859 | 534 | 1001 | 1042 | 278 | 0.8595 | 0.766 | 2987 |
| kumo_tabular_q7 (teacher) | 686 | 275 | 827 | 955 | 213 | 0.8918 | 0.959 | 4298 |
| KD CutMix 2:1 (paper recipe) | 847 | 524 | 969 | 1049 | 273 | 0.8625 | 0.719 | 2584 |
| KD real rows only | 846 | 510 | 976 | 1053 | 341 | 0.7876 | 0.387 | 956 |
| KD real rows only + constant shift, median kept | 848 | 510 | 976 | 1059 | 266 | 0.8705 | 0.902 | 3810 |
| KD out-of-fold targets, CutMix 2:1 | 905 | 544 | 1031 | 1139 | 275 | 0.8628 | 0.942 | 5256 |
| KD lag diffs + residual, CutMix 2:1 | 763 | 371 | 897 | 1019 | 253 | 0.8699 | 0.662 | 2085 |
| KD lag diffs + residual, CutMix 2:1 + constant shift, median kept | 765 | 371 | 901 | 1022 | 240 | 0.8857 | 0.886 | 3438 |
| hgb_q7 + lag diffs + residual (labels) | 747 | 320 | 913 | 1008 | 245 | 0.8742 | 0.763 | 2583 |
| hgb_q7 + lag diffs + residual + spline recal, median kept | 747 | 320 | 913 | 1008 | 232 | 0.8854 | 0.911 | 3761 |

[cutmix]: https://github.com/ogrisel/cursor-sandbox/blob/a487de66824903384aeb82cd66bfaa4f2ef2f53a/kumo_distillation/scripts/folds.py#L156-L168
[training-set]: https://github.com/ogrisel/cursor-sandbox/blob/a487de66824903384aeb82cd66bfaa4f2ef2f53a/kumo_distillation/scripts/distill.py#L103-L141
[fit-predict]: https://github.com/ogrisel/cursor-sandbox/blob/a487de66824903384aeb82cd66bfaa4f2ef2f53a/kumo_distillation/scripts/distill.py#L144-L169
[gen-teacher]: https://github.com/ogrisel/cursor-sandbox/blob/a487de66824903384aeb82cd66bfaa4f2ef2f53a/kumo_distillation/scripts/gen_teacher.py#L49-L88
[gen-teacher-oof]: https://github.com/ogrisel/cursor-sandbox/blob/a487de66824903384aeb82cd66bfaa4f2ef2f53a/kumo_distillation/scripts/gen_teacher_oof.py#L39-L61
[lag-diffs]: https://github.com/ogrisel/cursor-sandbox/blob/a487de66824903384aeb82cd66bfaa4f2ef2f53a/kumo_distillation/scripts/folds.py#L128-L149
[last-load]: https://github.com/ogrisel/cursor-sandbox/blob/a487de66824903384aeb82cd66bfaa4f2ef2f53a/kumo_distillation/scripts/folds.py#L115-L125
[recalibrate]: https://github.com/ogrisel/cursor-sandbox/blob/a487de66824903384aeb82cd66bfaa4f2ef2f53a/kumo_distillation/scripts/calibrate.py#L53-L80
