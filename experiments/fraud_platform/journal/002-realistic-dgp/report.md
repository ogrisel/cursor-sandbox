# 002 — Critical review of 001 and a harder, more mechanistic simulator

## Critical review of iteration 001

Iteration 001 ran end to end, but did not serve the educational goal well:

| Problem in 001 | Why it matters | Priority |
| --- | --- | --- |
| ROC AUC ≈ 1.000 for every model. A new device (< 3 days) and a foreign IP almost perfectly separated fraud from legitimate traffic. | When everything is perfect there is nothing to learn about delayed labels, censoring or features. The €277 "oracle gap" was noise. | 1 |
| Window aggregates were computed in a hand-written Python loop. The backtest was a row-count `TimeSeriesSplit` with an arbitrary 2,000-row gap. | The task asks for `skrub`-based time feature engineering and backtesting. A row gap is not a calendar quantity, and label availability (system lag) was handled outside the split. | 2 |
| No baselines (approve all, legacy rules, perfect clairvoyant), no calibration check, no comparison of "what a practitioner would measure" against the truth. | Business impact cannot be read without reference points. The cost-optimal threshold assumes calibrated probabilities, and censored training sets are not calibrated. | 3 |
| No feature uses past *labels*, so label delay never mattered for features. | Known-fraud aggregates (for example a merchant's chargeback rate) are standard and are exactly where system lag causes leakage bugs. | 2 (folded in) |
| No exploration (random reviews or approvals), so no unbiased off-policy evaluation. | This is the principled fix for selection bias, but it needs a closed-loop simulation. | 4 (next steps) |
| Single seed, few positives per fold, no uncertainty. | Small differences are not interpretable. | 4 |
| Repository layout: Pixi project at the repository root. | Experiments should be self-contained. | Housekeeping (done) |

Iterations 002–004 address priorities 1–3.

## What changed in the simulator

The new simulator (`src/fraud_sim/simulator.py`) is still vectorised and runs in about 1.5 s for 200k attempts.

- **Entities.** 6,000 customers with heavy-tailed activity, a personal spending scale, four favourite shops, a long-lived primary device, and some accounts opened during the period. There are 40 shops in 8 categories, each with an amount multiplier and a *fraud appeal* (weak checkout security).
- **Legitimate noise that overlaps fraud signals.** 5% of legitimate payments come from a brand-new device, and 5% from abroad (travel).
- **Three fraud modus operandi**, organised in campaigns that hit 1–3 stolen cards each:
  - *card testing*: 2–5 micro-payments (€0.5–5) on a digital shop within 30 minutes, followed by cash-out attempts;
  - *cash-out*: 1–4 larger payments over up to 48 hours;
  - *stealth account takeover*: the fraudster uses the victim's own device and country and spends about 2× the victim's usual amount over a week.
- **Adaptive fraudsters (concept drift).** The share of campaigns using a foreign IP falls linearly from 70% to 25% over the 180 days, eroding the main legacy rule. 25% of fraud attempts spoof an old device fingerprint.
- **Legacy policy.** A rule score with noise. It declines above a threshold, sends the riskiest remaining attempts to an analyst queue with a *daily capacity* of 20 reviews, and approves the rest.
- **Feedback.** Review verdicts arrive 2–3 days later. Chargebacks arrive with a log-normal delay (median ≈ 18 days, long tail) for 80% of approved fraud. 0.1% of legitimate approved payments are disputed as fraud (friendly fraud, i.e. label noise). Declined attempts are never labelled.

Generated history (seed 0):

| Quantity | Value | Real-world anchor |
| --- | ---: | --- |
| Attempts over 180 days | 201,204 | — |
| Daily volume | ≈ €93k | Small platform |
| Attempted-fraud rate (count) | 0.43% | — |
| Realized fraud rate after legacy (count / value) | 0.24% / 0.37% | EU card fraud is 0.015% / 0.033% overall ([EBA–ECB 2025](https://www.ecb.europa.eu/press/intro/publications/pdf/ecb.ebaecb202512.en.pdf)), with card-not-present payments far above average. We are about 10× higher on purpose, to have about 100 test frauds per 3-week fold. |
| Fraud stopped by legacy rules | 44% | — |
| Fraud mix (card testing / cash-out / stealth) | 495 / 294 / 78 | — |

## Difficulty check

Four calendar folds (cutoffs on days 96, 117, 138 and 159, each followed by a 21-day test window). There is no tuning, and the model is a default `HistGradientBoostingClassifier`. "Censored" trains on the labels that are *known at the cutoff* (`fraud_sim.backtest.label_as_known_at`). "Oracle" trains on the private ground truth of all past attempts, including declined ones. All rows are scored on the full ground truth of the test window.

Mean (std) over the 4 folds:

| Model | Features | ROC AUC | Average precision |
| --- | --- | ---: | ---: |
| Legacy rule score | — | 0.838 (0.045) | 0.111 (0.045) |
| HGB, censored labels | row-level | 0.885 (0.026) | 0.367 (0.008) |
| HGB, censored labels | row + windows | 0.821 (0.014) | 0.586 (0.068) |
| HGB, oracle labels | row-level | 0.831 (0.099) | 0.286 (0.073) |
| HGB, oracle labels | row + windows | 0.928 (0.029) | 0.660 (0.055) |

Raw values: [`fold_metrics.csv`](fold_metrics.csv), [`summary.json`](summary.json).

## Analysis

- The problem is no longer trivial. The legacy score ranks well globally (ROC AUC 0.84) but is very imprecise at the top (AP 0.11). That is typical of rule engines, and it is what makes the analyst queue expensive.
- Window features carry most of the signal (AP +0.2 to +0.4): velocity of card testing, device reuse across victims, and spending relative to the customer's own 30-day mean.
- With window features, the censored model loses about 0.1 ROC AUC and 0.07 AP relative to the oracle. The ROC AUC loss comes from the region the legacy policy *declined*: those attempts are absent from the censored training set, so the model has to extrapolate there.
- With only about 100 test frauds per fold, the fold-to-fold standard deviation is 0.03–0.10. Differences smaller than that should not be read as findings. Iteration 004 reports per-fold paired differences.

Runtime: 8 s end to end (simulation + features 4.3 s, 16 model fits).

Next: [iteration 003](../003-skrub-dataops/report.md) moves feature engineering and backtesting into `skrub` and adds lag-aware label features.
