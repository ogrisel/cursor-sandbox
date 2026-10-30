# 001 — Delayed-feedback payment fraud backtest

> **Superseded.** Every model reached ROC AUC ≈ 1, so the comparisons below carry no information. See the critical review in [002](../002-realistic-dgp/report.md). The code for this iteration is at commit `2934bf3`.

## Purpose

Build a fast, inspectable data-generating process for online card-not-present
fraud over a shared payment platform, rather than presenting an unrealistic
i.i.d. classification dataset. The simulator is deliberately an educational
test bed, not a calibrated representation of any provider.

## Literature review and design choices

| Evidence | Implication in this experiment |
| --- | --- |
| The [EBA/ECB 2025 payment-fraud report](https://www.ecb.europa.eu/press/intro/publications/pdf/ecb.ebaecb202512.en.pdf) reports 17.06m fraudulent card transactions out of 111.05bn EU/EEA attempts in 2024 (0.015% by count) and a 0.033% value rate. | Fraud attempts are rare and amounts are euro-denominated, positive and skewed. The 0.36% simulated attempt rate is intentionally higher than the reported realized rate, to yield enough positives in a short run and to represent pre-decision attempts. It should not be interpreted as an EEA population estimate. |
| [Dal Pozzolo et al. (2015)](https://doi.org/10.1109/IJCNN.2015.7280527) describe delayed labels, constrained investigation, and drift in real card-fraud operations. | Review labels arrive after two days; chargeback feedback has a 7–22 day lag. A model only trains on labels available by each fold's deployment instant. |
| [Soemers et al. (2018)](https://doi.org/10.1609/aaai.v32i1.11411) frame fraud handling as an exploration/exploitation problem: deterministic alert selection obscures the unreviewed population. | The legacy policy blocks high-risk attempts, permanently censoring their counterfactual outcomes. Approved payments mature after 25 days; unreported fraud is therefore incorrectly retained as legitimate. |
| [Bahnsen et al. (2021)](https://doi.org/10.1016/j.ejor.2021.05.028) treat fraud as instance-dependent cost-sensitive learning. The [Probabl tutorial](https://probabl-ai.github.io/calibration-cost-sensitive-learning/content/notebooks/cost_sensitive_learning.html) gives a transparent payment-gain formulation. | Evaluation uses monetary gain, not accuracy or ROC AUC alone. It earns 2% on approved legitimate volume, loses amount + €20 for accepted fraud, and loses €10 when declining legitimate customers. |

The second source also explains why this setup does **not** claim causal
counterfactual evaluation: rejected attempts lack a realizable public outcome.
The private simulator label is usable for a controlled upper-bound comparison,
but it is unavailable in a real production history.

## Mechanisms in the generated history

- 3,000 customers buy from 30 shops through one platform over 120 UTC days.
- Legitimate purchases follow shop popularity, day-hour seasonality, category
  price distributions, customer countries and persistent devices.
- Fraud rings reuse compromised customer identities, a small device pool, and
  bursts across one to three shops within 70 minutes. Their amounts overlap
  with legitimate retail purchases; foreign/new-device signals are useful but
  noisy.
- The legacy policy produces `approved`, `reviewed`, or `declined` actions.
  Only reviewed cases and delayed reports reveal labels. Declined cases are
  visible as attempts but never acquire an outcome.
- Features are strictly pre-decision rolling counts/sums for customer,
  merchant, and device histories. The implementation trims each in-memory
  history before appending the current payment, so it does not include the
  current row or future rows.

The generated timestamped history retains `is_fraud` solely as a private
simulator truth column; a production-style modelling input must remove it.
The compressed dump is not in this branch, so the report job does not check
it out. Commit `2934bf3` still has the generator.

## Modelling and backtesting

Each expanding fold uses `TimeSeriesSplit` plus a 2,000-transaction gap.
This is the appropriate time-aware splitter documented in the
[skrub session example](https://skrub-data.org/stable/auto_examples/0110_session_encoder.html);
`skrub` itself does not provide a `TimeGapSplit` API. Within each fold,
`skrub.TableVectorizer` and `skrub.DatetimeEncoder` build hour, weekday, and
circular calendar features, then `HistGradientBoostingClassifier` fits the
candidate. This matters: fitting the vectorizer inside the fold prevents
future category/date transformations leaking into the past.

`censored_history` sees only operationally observable outcomes. `private_oracle`
has the simulator's latent truth for every historical attempt, including
declines. Both are scored on the same complete, later held-out population.

| Model | Mean AP | Mean ROC AUC | Total test gain (€) | Difference from oracle (€) |
| --- | ---: | ---: | ---: | ---: |
| Censored history | 0.979 | 1.000 | 359,076 | -277 |
| Private oracle | 0.995 | 1.000 | 359,353 | 0 |

The exact fold-level values are recorded in
[`data/backtest_results.csv`](data/backtest_results.csv), with provenance and
rates in [`data/summary.json`](data/summary.json).

## Interpretation and limitations

The oracle has better mean ranking and higher total business gain, but the
short synthetic run has an intentionally structured fraud process, so both
models obtain very high ROC AUC. The €277 gap is a lower-bound illustration,
not a claim about deployment value; it varies by random seed, fraud strategy,
review rate, latency, and the cost assumptions.

The cost policy is fixed before test scoring rather than tuned on test labels.
For a payment with amount `a` and calibrated fraud probability `p`, it blocks
when:

`p >= (10 + 0.02a) / (30 + 1.02a)`.

This follows directly from the stated gains/costs. It still assumes calibrated
probabilities and a static cost matrix. It does not represent customer
heterogeneity, partial recoveries, strong customer authentication, adaptive
fraudsters, manual-review capacity, legal constraints, or off-policy
correction. A serious next experiment should add randomized low-risk review
exploration and inverse-propensity/off-policy evaluation rather than treat the
observed label set as representative.
