"""Business value of authorisation policies.

The gain matrix follows the cost-sensitive learning tutorial by probabl
(https://probabl-ai.github.io/calibration-cost-sensitive-learning/) with
instance-dependent amounts (Correa Bahnsen et al. 2013; Vanderschueren et al. 2022),
extended with a capacity-limited manual review action:

============  =====================  ==================
action        legitimate payment     fraudulent payment
============  =====================  ==================
approve       + commission * amount  - amount - fraud_fee
decline       - false_decline_cost   0
review        + commission * amount  0
              - review_cost          - review_cost
============  =====================  ==================
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

APPROVE, DECLINE, REVIEW = 0, 1, 2


@dataclass(frozen=True)
class Costs:
    commission: float = 0.02
    fraud_fee: float = 20.0
    false_decline_cost: float = 10.0
    review_cost: float = 5.0
    review_capacity_per_day: int = 20


def action_values(p: np.ndarray, amount: np.ndarray, c: Costs) -> np.ndarray:
    """Expected gain of each action given a fraud probability, shape (n, 3)."""
    approve = (1 - p) * c.commission * amount - p * (amount + c.fraud_fee)
    decline = -(1 - p) * c.false_decline_cost
    review = (1 - p) * c.commission * amount - c.review_cost
    return np.stack([approve, decline, review], axis=1)


def decide(tx: pd.DataFrame, p: np.ndarray, c: Costs, threshold_scale: float = 1.0) -> np.ndarray:
    """Bayes-optimal actions under a daily review capacity.

    ``threshold_scale`` rescales the odds of ``p`` before deciding. A value of
    1 trusts the probabilities; other values mimic a deliberately more or less
    aggressive operating point, which is what miscalibration does implicitly.
    """
    odds = p / np.clip(1 - p, 1e-12, None) * threshold_scale
    p = odds / (1 + odds)
    values = action_values(p, tx["amount_eur"].to_numpy(), c)
    action = np.argmax(values[:, :2], axis=1)
    review_gain = values[:, REVIEW] - values[:, :2].max(axis=1)
    candidates = review_gain > 0
    day = tx["timestamp"].dt.floor("D").to_numpy()
    rank = pd.Series(np.where(candidates, -review_gain, np.inf)).groupby(day).rank(method="first").to_numpy()
    action[candidates & (rank <= c.review_capacity_per_day)] = REVIEW
    return action


def decide_on_top_of_legacy(tx: pd.DataFrame, p: np.ndarray, c: Costs) -> np.ndarray:
    """Keep legacy declines and reviews; the model can only decline more."""
    action = legacy_actions(tx)
    values = action_values(p, tx["amount_eur"].to_numpy(), c)
    extra_decline = (action == APPROVE) & (values[:, DECLINE] > values[:, APPROVE])
    action[extra_decline] = DECLINE
    return action


def legacy_actions(tx: pd.DataFrame) -> np.ndarray:
    return np.select(
        [tx["decision"].eq("declined").to_numpy(), tx["decision"].str.startswith("review").to_numpy()],
        [DECLINE, REVIEW],
        APPROVE,
    )


def realised_gain(action: np.ndarray, is_fraud: np.ndarray, amount: np.ndarray, c: Costs) -> np.ndarray:
    legit = ~is_fraud
    return np.select(
        [action == APPROVE, action == DECLINE, action == REVIEW],
        [
            np.where(legit, c.commission * amount, -amount - c.fraud_fee),
            np.where(legit, -c.false_decline_cost, 0.0),
            np.where(legit, c.commission * amount, 0.0) - c.review_cost,
        ],
    )


def observable_labels(tx: pd.DataFrame) -> pd.Series:
    """Labels a practitioner has for the test window once it has matured.

    Declined attempts stay unlabelled; approved payments without a chargeback
    count as legitimate; friendly-fraud disputes count as fraud.
    """
    label = pd.Series(np.nan, index=tx.index)
    reviewed = tx["decision"].str.startswith("review")
    label[reviewed] = tx.loc[reviewed, "is_fraud"].astype(float)
    approved = tx["decision"].eq("approved")
    label[approved] = tx.loc[approved, "observed_label"].fillna(0.0)
    return label
