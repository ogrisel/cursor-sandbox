"""Calendar backtesting with label availability at each deployment cutoff."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class BacktestConfig:
    first_cutoff_day: int = 96
    test_days: int = 21
    n_folds: int = 4
    # Approved payments without a chargeback are treated as legitimate only
    # once they are old enough for most chargebacks to have arrived.
    maturity_days: int = 45


def fold_cutoffs(tx: pd.DataFrame, cfg: BacktestConfig) -> list[pd.Timestamp]:
    start = tx["timestamp"].min().floor("D")
    return [start + pd.Timedelta(days=cfg.first_cutoff_day + k * cfg.test_days) for k in range(cfg.n_folds)]


def label_as_known_at(tx: pd.DataFrame, cutoff: pd.Timestamp, maturity_days: int) -> pd.Series:
    """Training label available to the platform at ``cutoff`` (NaN if none).

    - reviewed attempts: the analyst verdict, once it has arrived;
    - approved attempts: 1 if a chargeback has arrived; 0 if the payment is
      older than the maturity window and no chargeback arrived. Unreported
      fraud is therefore silently mislabelled as legitimate;
    - declined attempts: never labelled (counterfactual censoring).
    """
    arrived = tx["label_observed_at"] < cutoff
    label = pd.Series(np.nan, index=tx.index)
    reviewed = tx["decision"].str.startswith("review")
    label[reviewed & arrived] = tx.loc[reviewed & arrived, "observed_label"]
    approved = tx["decision"].eq("approved") & (tx["timestamp"] < cutoff)
    label[approved & arrived] = 1.0
    matured = approved & ~arrived & (tx["timestamp"] < cutoff - pd.Timedelta(days=maturity_days))
    label[matured] = 0.0
    return label


def iter_folds(tx: pd.DataFrame, cfg: BacktestConfig):
    """Yield ``(cutoff, train_mask_censored, train_mask_oracle, test_mask, y_censored)``."""
    for cutoff in fold_cutoffs(tx, cfg):
        test = (tx["timestamp"] >= cutoff) & (tx["timestamp"] < cutoff + pd.Timedelta(days=cfg.test_days))
        y_cens = label_as_known_at(tx, cutoff, cfg.maturity_days)
        yield cutoff, y_cens.notna().to_numpy(), (tx["timestamp"] < cutoff).to_numpy(), test.to_numpy(), y_cens
