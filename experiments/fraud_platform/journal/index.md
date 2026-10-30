# Shared payment-platform fraud simulator

An educational, fast-running simulator of card-not-present payments on a payment platform shared by 40 online shops. A legacy rule engine is already deployed, and labels are delayed, incomplete, noisy and censored by that engine's own decisions. On top of the simulator, a `skrub` + `HistGradientBoostingClassifier` pipeline with point-in-time window features is backtested on calendar folds, and evaluated in euros against the private ground truth that only a simulation provides.

## Main findings (seed 0, 4 × 21-day test windows)

| Question | Answer | Iteration |
| --- | --- | --- |
| Do window aggregates matter? | Yes. AP 0.43 → 0.72 for the censored model (legacy rule score alone: 0.11). | [003](003-skrub-dataops/report.md) |
| Do label-based features help despite label delay? | No. Lag-aware versions cost 0.015–0.044 AP in every fold. | [003](003-skrub-dataops/report.md) |
| What does back-dating labels in features do? | It wins offline in 2 of 4 folds and loses 0.07–0.23 AP once served. | [003](003-skrub-dataops/report.md) |
| How much ranking quality does censoring cost? | 0.06–0.11 AP versus a model trained on the private labels. | [003](003-skrub-dataops/report.md) |
| How much money does censoring cost? | Nothing measurable: +€32.0k vs +€31.8k uplift over the legacy rules (67% of the clairvoyant uplift for both). | [004](004-business-evaluation/report.md) |
| How wrong is evaluation on observable labels? | It underestimates the uplift by 26%. | [004](004-business-evaluation/report.md) |
| Replace the rules or layer the model on top? | Replacing earns €11.7k more over 84 days, but this is only verifiable in simulation. | [004](004-business-evaluation/report.md) |

## Iterations

- [001 — first simulator, causal features and backtest](001-simulator/report.md) (superseded: the problem was trivially separable)
- [002 — critical review, mechanistic v2 simulator, difficulty check](002-realistic-dgp/report.md)
- [003 — skrub DataOps, lag-aware label features and leakage](003-skrub-dataops/report.md)
- [004 — business evaluation, evaluation bias and calibration](004-business-evaluation/report.md)

## Reproduce

```bash
cd experiments/fraud_platform
pixi run test       # point-in-time and simulator tests
pixi run iter004    # about 20 s: simulate, feature store, backtests, policies, plots
```
