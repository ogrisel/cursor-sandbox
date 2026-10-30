"""Point-in-time feature engineering on the platform event log.

Every feature for an attempt at time ``t`` only uses information that the
platform has at ``t``:

- window aggregates over *earlier* attempts (``closed="left"``), including the
  legacy decisions on those attempts, which are known immediately;
- feedback (reviews, chargebacks) only once it has *arrived*, i.e. with
  ``label_observed_at < t``. This is the system lag: a chargeback filed in
  three weeks cannot inform a decision taken today.

The ``leaky_*`` columns deliberately break the second rule: they index labels
by the transaction time instead of the arrival time. This is a common bug in
offline feature pipelines; the columns are kept to measure its effect.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

FOREIGN_NON_EU = ["GB", "US", "RU", "NG", "BR"]


def rolling_by_key(
    tx: pd.DataFrame, key: str, window: str, column: str = "amount_eur", agg: str = "count"
) -> np.ndarray:
    """Aggregate ``column`` over strictly earlier attempts of the same ``key``."""
    order = np.lexsort((tx["timestamp"].to_numpy(), tx[key].to_numpy()))
    sorted_tx = tx.iloc[order]
    rolled = (
        sorted_tx.set_index("timestamp")
        .groupby(key, sort=True)[column]
        .rolling(window, closed="left")
        .agg(agg)
    )
    out = np.empty(len(tx))
    out[order] = rolled.to_numpy()
    return np.nan_to_num(out, nan=0.0) if agg in ("count", "sum") else out


def seconds_since_previous(tx: pd.DataFrame, key: str) -> np.ndarray:
    previous = tx.groupby(key)["timestamp"].shift()
    return (tx["timestamp"] - previous).dt.total_seconds().to_numpy()


def arrived_label_count(
    tx: pd.DataFrame, key: str, window: pd.Timedelta, by: str = "label_observed_at"
) -> np.ndarray:
    """Count fraud labels on ``key`` that are known at each attempt time.

    With ``by="label_observed_at"`` a label is usable once it has arrived. With
    ``by="timestamp"`` the label is (wrongly) back-dated to the payment time.
    """
    positives = tx.loc[tx["observed_label"].eq(1.0), [key, by]].dropna()
    positives = positives.rename(columns={by: "event_time"}).sort_values("event_time")
    positives["event_time"] = positives["event_time"].astype("datetime64[ns, UTC]")
    positives["cum"] = positives.groupby(key).cumcount() + 1
    queries = tx[[key, "timestamp"]].reset_index(drop=True).assign(pos=np.arange(len(tx)))
    result = np.zeros(len(tx))
    for lag, sign in ((pd.Timedelta(0), 1.0), (window, -1.0)):
        event_time = (queries["timestamp"] - lag).astype("datetime64[ns, UTC]")
        q = queries.assign(event_time=event_time).drop(columns="timestamp")
        q = q.sort_values("event_time", kind="stable")
        merged = pd.merge_asof(
            q, positives, on="event_time", by=key, allow_exact_matches=False, direction="backward"
        )
        result[merged["pos"].to_numpy()] += sign * merged["cum"].fillna(0).to_numpy()
    return result


def add_window_features(tx: pd.DataFrame) -> pd.DataFrame:
    """Velocity and spending-profile features from earlier attempts."""
    tx = tx.sort_values("timestamp", kind="stable").reset_index(drop=True)
    tx = tx.assign(was_declined=tx["decision"].isin(["declined", "review_blocked"]).astype(float))
    out = pd.DataFrame(index=tx.index)
    out["cust_n_1h"] = rolling_by_key(tx, "customer_id", "1h")
    out["cust_n_24h"] = rolling_by_key(tx, "customer_id", "24h")
    out["cust_amount_24h"] = rolling_by_key(tx, "customer_id", "24h", agg="sum")
    out["cust_mean_amount_30d"] = rolling_by_key(tx, "customer_id", "30D", agg="mean")
    out["amount_to_cust_mean_30d"] = tx["amount_eur"] / out["cust_mean_amount_30d"]
    out["cust_declined_24h"] = rolling_by_key(tx, "customer_id", "24h", column="was_declined", agg="sum")
    out["cust_seconds_since_prev"] = seconds_since_previous(tx, "customer_id")
    out["device_n_24h"] = rolling_by_key(tx, "device_id", "24h")
    out["device_n_7d"] = rolling_by_key(tx, "device_id", "7D")
    out["merchant_n_1h"] = rolling_by_key(tx, "merchant_id", "1h")
    out["merchant_n_7d"] = rolling_by_key(tx, "merchant_id", "7D")
    out["merchant_burst"] = out["merchant_n_1h"] / (out["merchant_n_7d"] / 168 + 1)
    out["ip_mismatch"] = tx["ip_country"].ne(tx["customer_country"]).astype(float)
    out["ip_non_eu"] = tx["ip_country"].isin(FOREIGN_NON_EU).astype(float)
    return pd.concat([tx.drop(columns="was_declined"), out.astype("float32")], axis=1)


def add_feedback_features(tx: pd.DataFrame) -> pd.DataFrame:
    """Aggregate fraud labels that have arrived, plus back-dated leaky twins.

    Each ``known_*`` column has a ``leaky_*`` twin computed identically except
    that labels are indexed by payment time. The twins are only meant to
    measure how much an offline backtest overstates such a feature.
    """
    tx = tx.sort_values("timestamp", kind="stable").reset_index(drop=True)
    month, week = pd.Timedelta(days=30), pd.Timedelta(days=7)
    merchant_n_30d = rolling_by_key(tx, "merchant_id", "30D") + 1
    out = {}
    for prefix, by in (("known", "label_observed_at"), ("leaky", "timestamp")):
        out[f"{prefix}_merchant_fraud_rate_30d"] = arrived_label_count(tx, "merchant_id", month, by) / merchant_n_30d
        out[f"{prefix}_card_fraud_7d"] = arrived_label_count(tx, "customer_id", week, by)
        out[f"{prefix}_device_fraud_90d"] = arrived_label_count(tx, "device_id", 3 * month, by)
    return tx.assign(**{k: np.asarray(v, dtype="float32") for k, v in out.items()})
