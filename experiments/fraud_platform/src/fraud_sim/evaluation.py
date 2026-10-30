"""Scorers for ``skrub.cross_validate`` that read the private test truth."""

from __future__ import annotations

import pandas as pd
from sklearn.metrics import average_precision_score, brier_score_loss, roc_auc_score

from .pipeline import KNOWN_LABEL_FEATURES, LEAKY_LABEL_FEATURES


def as_backtested(X: pd.DataFrame, y: pd.DataFrame) -> pd.DataFrame:
    return X


def as_served(X: pd.DataFrame, y: pd.DataFrame) -> pd.DataFrame:
    """Replace back-dated label features by the values that exist at decision time.

    Once deployed, a label aggregate can only count labels that have arrived,
    whatever the offline pipeline computed. The lag-aware values travel in the
    target frame because the leaky model does not take them as inputs.
    """
    swap = {leaky: y[known] for leaky, known in zip(LEAKY_LABEL_FEATURES, KNOWN_LABEL_FEATURES) if leaky in X}
    return X.assign(**swap)


def _scorer(metric, view):
    def scorer(learner, X, y):
        return metric(y["is_fraud"].to_numpy(), learner.predict_proba(view(X, y))[:, 1])
    return scorer


def _calibration_ratio(learner, X, y):
    """Expected number of frauds predicted by the model over the actual number."""
    return float(learner.predict_proba(X)[:, 1].sum() / y["is_fraud"].sum())


def ranking_scorers() -> dict:
    return {
        "ap": _scorer(average_precision_score, as_backtested),
        "roc_auc": _scorer(roc_auc_score, as_backtested),
        "brier": _scorer(brier_score_loss, as_backtested),
        "calibration_ratio": _calibration_ratio,
        "ap_served": _scorer(average_precision_score, as_served),
        "roc_auc_served": _scorer(roc_auc_score, as_served),
    }
