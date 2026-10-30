"""Fast, causal simulator and backtest for a shared online-payment platform.

The public historical table intentionally has incomplete, delayed labels.  The
private ``is_fraud`` column exists only to evaluate experiments and an oracle
upper bound; it must not be included in a deployable feature table.
"""

from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import average_precision_score, roc_auc_score
from sklearn.model_selection import TimeSeriesSplit
from sklearn.pipeline import make_pipeline
from skrub import DatetimeEncoder, TableVectorizer


@dataclass(frozen=True)
class SimulationConfig:
    """Parameters selected for quick runs with a rare attempted-fraud rate."""

    seed: int = 7
    n_days: int = 120
    attempts_per_day: int = 1_500
    n_customers: int = 3_000
    n_merchants: int = 30


def _timestamps(rng: np.random.Generator, day: pd.Timestamp, n: int) -> pd.DatetimeIndex:
    """Draw online-shopping times, concentrating activity in waking hours."""
    hour_weights = np.array(
        [0.007, 0.004, 0.003, 0.003, 0.004, 0.008, 0.020, 0.040, 0.055, 0.060, 0.060, 0.060,
         0.060, 0.065, 0.065, 0.065, 0.070, 0.075, 0.075, 0.070, 0.060, 0.045, 0.025, 0.014]
    )
    hours = rng.choice(
        24,
        size=n,
        p=hour_weights / hour_weights.sum(),
    )
    seconds = hours * 3600 + rng.integers(0, 3600, n)
    return day + pd.to_timedelta(seconds, unit="s")


def simulate(config: SimulationConfig = SimulationConfig()) -> pd.DataFrame:
    """Generate attempted card-not-present transactions and delayed policy feedback.

    Fraud rings reuse compromised customer identities, foreign devices and short
    merchant bursts. The legacy platform blocks some attempts; therefore their
    counterfactual fraud outcome is permanently censored in the public history.
    """
    rng = np.random.default_rng(config.seed)
    days = pd.date_range("2025-01-01", periods=config.n_days, freq="D", tz="UTC")
    merchant_ids = np.array([f"shop_{i:02d}" for i in range(config.n_merchants)])
    merchant_category = np.array(["fashion", "digital", "travel", "marketplace", "home"])[
        np.arange(config.n_merchants) % 5
    ]
    merchant_weights = rng.dirichlet(np.ones(config.n_merchants) * 2.5)
    customer_country = rng.choice(["FR", "DE", "ES", "IT", "NL"], config.n_customers)
    customer_ids = np.array([f"cust_{i:05d}" for i in range(config.n_customers)])
    rows: list[pd.DataFrame] = []

    for day_i, day in enumerate(days):
        n_legit = rng.poisson(config.attempts_per_day)
        customers = rng.choice(customer_ids, n_legit)
        customer_pos = np.fromiter((int(c.split("_")[1]) for c in customers), int, count=n_legit)
        merchants = rng.choice(merchant_ids, n_legit, p=merchant_weights)
        merchant_pos = np.fromiter((int(m.split("_")[1]) for m in merchants), int, count=n_legit)
        categories = merchant_category[merchant_pos]
        # Euro amounts are positively skewed and category-sensitive.
        amount_scale = np.select(
            [categories == "travel", categories == "digital", categories == "fashion"],
            [5.5, 3.6, 4.1],
            default=4.4,
        )
        legit = pd.DataFrame(
            {
                "timestamp": _timestamps(rng, day, n_legit),
                "customer_id": customers,
                "merchant_id": merchants,
                "merchant_category": categories,
                "amount_eur": np.round(rng.lognormal(amount_scale, 0.65), 2),
                "country": customer_country[customer_pos],
                "ip_country": np.where(
                    rng.random(n_legit) < 0.04,
                    rng.choice(["GB", "CH", "US"], n_legit),
                    customer_country[customer_pos],
                ),
                "device_age_days": rng.gamma(5, 35, n_legit).round(1),
                "is_fraud": False,
            }
        )
        # Attacks cluster in rings and are deliberately only moderately larger:
        # this gives transaction frequency and cross-shop behavior real value.
        n_rings = rng.poisson(1.3)
        fraud_parts: list[pd.DataFrame] = []
        for ring in range(n_rings):
            n_attempts = int(rng.integers(2, 8))
            compromised = rng.choice(customer_ids, n_attempts)
            merchant_pool = rng.choice(merchant_ids, size=rng.integers(1, 4), replace=False)
            attack_merchants = rng.choice(merchant_pool, n_attempts)
            attack_pos = np.fromiter(
                (int(m.split("_")[1]) for m in attack_merchants), int, count=n_attempts
            )
            attack_categories = merchant_category[attack_pos]
            base_time = day + pd.to_timedelta(rng.integers(8 * 3600, 23 * 3600), unit="s")
            fraud_parts.append(
                pd.DataFrame(
                    {
                        "timestamp": base_time
                        + pd.to_timedelta(np.sort(rng.integers(0, 70 * 60, n_attempts)), unit="s"),
                        "customer_id": compromised,
                        "merchant_id": attack_merchants,
                        "merchant_category": attack_categories,
                        "amount_eur": np.round(rng.lognormal(4.45, 0.55, n_attempts), 2),
                        "country": customer_country[
                            np.fromiter((int(c.split("_")[1]) for c in compromised), int, count=n_attempts)
                        ],
                        "ip_country": np.where(
                            rng.random(n_attempts) < 0.72,
                            rng.choice(["GB", "RO", "NG", "US"], n_attempts),
                            customer_country[
                                np.fromiter(
                                    (int(c.split("_")[1]) for c in compromised),
                                    int,
                                    count=n_attempts,
                                )
                            ],
                        ),
                        "device_age_days": rng.exponential(3, n_attempts).round(1),
                        "is_fraud": True,
                    }
                )
            )
        rows.append(pd.concat([legit, *fraud_parts], ignore_index=True))

    tx = pd.concat(rows, ignore_index=True).sort_values("timestamp", kind="stable").reset_index(drop=True)
    tx.insert(0, "transaction_id", [f"tx_{i:07d}" for i in range(len(tx))])
    tx["amount_eur"] = tx["amount_eur"].clip(1, 2_500)
    tx["is_cross_border"] = tx["country"].ne(tx["ip_country"])
    tx["device_id"] = np.where(
        tx["is_fraud"],
        "fraud_device_" + (np.arange(len(tx)) % 55).astype(str),
        "device_" + tx["customer_id"].str.removeprefix("cust_"),
    )

    # A deployed, imperfect policy creates the historical selection mechanism.
    legacy_risk = (
        0.05
        + 0.54 * tx["is_cross_border"].astype(float)
        + 0.20 * (tx["device_age_days"] < 3).astype(float)
        + 0.10 * (tx["merchant_category"] == "digital").astype(float)
        + 0.06 * (tx["amount_eur"] > 350).astype(float)
        + rng.normal(0, 0.12, len(tx))
    ).clip(0, 1)
    tx["legacy_score"] = legacy_risk
    tx["decision"] = np.select(
        [legacy_risk >= 0.72, legacy_risk >= 0.51],
        ["declined", "reviewed"],
        default="approved",
    )
    reviewed = tx["decision"].eq("reviewed")
    approved_fraud = tx["decision"].eq("approved") & tx["is_fraud"]
    tx["label_observed_at"] = pd.Series(pd.NaT, index=tx.index, dtype="datetime64[ns, UTC]")
    tx.loc[reviewed, "label_observed_at"] = tx.loc[reviewed, "timestamp"] + pd.Timedelta(days=2)
    # Fraud reports take 7--22 days, while 15% are never reported at all.
    report_delay = pd.to_timedelta(rng.integers(7, 23, len(tx)), unit="D")
    reported = approved_fraud & (rng.random(len(tx)) < 0.85)
    tx.loc[reported, "label_observed_at"] = tx.loc[reported, "timestamp"] + report_delay[reported]
    tx["observed_fraud_label"] = np.where(
        tx["label_observed_at"].notna(), tx["is_fraud"].astype("float"), np.nan
    )
    return add_causal_features(tx)


def add_causal_features(tx: pd.DataFrame) -> pd.DataFrame:
    """Create pre-decision rolling features using strictly earlier attempts."""
    tx = tx.sort_values("timestamp", kind="stable").copy()
    histories: dict[tuple[str, str], deque[tuple[pd.Timestamp, float]]] = defaultdict(deque)
    features: defaultdict[str, list[float]] = defaultdict(list)
    for row in tx.itertuples(index=False):
        now = row.timestamp
        for name, key, window, amount in (
            ("customer_attempts_1d", ("customer", row.customer_id), pd.Timedelta(days=1), False),
            ("customer_amount_7d", ("customer_amount", row.customer_id), pd.Timedelta(days=7), True),
            ("merchant_attempts_1h", ("merchant", row.merchant_id), pd.Timedelta(hours=1), False),
            ("device_attempts_1d", ("device", row.device_id), pd.Timedelta(days=1), False),
        ):
            history = histories[key]
            while history and history[0][0] < now - window:
                history.popleft()
            features[name].append(sum(value for _, value in history) if amount else len(history))
            history.append((now, float(row.amount_eur)))
    for column, values in features.items():
        tx[column] = np.asarray(values, dtype="float32")
    return tx


FEATURE_COLUMNS = [
    "timestamp",
    "merchant_id",
    "merchant_category",
    "amount_eur",
    "country",
    "ip_country",
    "device_age_days",
    "is_cross_border",
    "customer_attempts_1d",
    "customer_amount_7d",
    "merchant_attempts_1h",
    "device_attempts_1d",
]


def make_model() -> object:
    """Use skrub's datetime engineering inside each fitted model pipeline."""
    vectorizer = TableVectorizer(
        datetime=DatetimeEncoder(
            resolution="hour", add_weekday=True, add_total_seconds=False, periodic_encoding="circular"
        ),
        cardinality_threshold=40,
        drop_if_unique=True,
    )
    return make_pipeline(
        vectorizer,
        HistGradientBoostingClassifier(
            learning_rate=0.08, max_leaf_nodes=31, l2_regularization=0.5, random_state=0
        ),
    )


def business_gain(y_true: np.ndarray, p_fraud: np.ndarray, amount: np.ndarray) -> tuple[float, float]:
    """Return a fixed cost-sensitive policy's gain and median threshold (EUR).

    Following cost-sensitive decision literature, accepting legitimate payments
    earns 2% commission; accepting fraud loses its amount plus €20 handling;
    blocking a legitimate payment costs €10 through support/churn.
    """
    # Block when its expected gain exceeds approval's expected gain:
    # -(1-p)*10 >= (1-p)*0.02*amount - p*(amount + 20).
    thresholds = (10.0 + 0.02 * amount) / (30.0 + 1.02 * amount)
    blocked = p_fraud >= thresholds
    gain = np.where(
        y_true,
        np.where(blocked, 0.0, -amount - 20.0),
        np.where(blocked, -10.0, 0.02 * amount),
    ).sum()
    return float(gain), float(np.median(thresholds))


def evaluate_backtest(tx: pd.DataFrame, n_splits: int = 3) -> pd.DataFrame:
    """Run chronological folds, contrasting censored history with private oracle labels."""
    tx = tx.sort_values("timestamp", kind="stable").reset_index(drop=True)
    splitter = TimeSeriesSplit(n_splits=n_splits, gap=2_000)
    rows: list[dict[str, object]] = []
    for fold, (train_idx, test_idx) in enumerate(splitter.split(tx), start=1):
        train, test = tx.iloc[train_idx].copy(), tx.iloc[test_idx].copy()
        # At the fold's deployment instant, labels not yet returned are unknown.
        cutoff = test["timestamp"].min()
        reviewed = train[
            train["decision"].eq("reviewed") & (train["label_observed_at"] < cutoff)
        ].copy()
        # An approved payment is conservatively made negative after a 25-day
        # chargeback window. Unreported fraud therefore becomes a false negative:
        # this models outcome censoring without peeking at the latent target.
        matured_approved = train[
            train["decision"].eq("approved") & (train["timestamp"] < cutoff - pd.Timedelta(days=25))
        ].copy()
        matured_approved["is_fraud"] = matured_approved["observed_fraud_label"].fillna(0).astype(bool)
        observed = pd.concat([reviewed, matured_approved], ignore_index=True)
        # The simulator-only oracle sees the true outcome even for declined attempts.
        for name, labelled_train in (("censored_history", observed), ("private_oracle", train)):
            if labelled_train["is_fraud"].nunique() < 2:
                continue
            model = make_model()
            model.fit(labelled_train[FEATURE_COLUMNS], labelled_train["is_fraud"])
            p = model.predict_proba(test[FEATURE_COLUMNS])[:, 1]
            y = test["is_fraud"].to_numpy()
            gain, threshold = business_gain(y, p, test["amount_eur"].to_numpy())
            rows.append(
                {
                    "fold": fold,
                    "model": name,
                    "train_rows": len(labelled_train),
                    "train_fraud_rate": labelled_train["is_fraud"].mean(),
                    "test_fraud_rate": y.mean(),
                    "average_precision": average_precision_score(y, p),
                    "roc_auc": roc_auc_score(y, p),
                    "cost_sensitive_gain_eur": gain,
                    "median_cost_threshold": threshold,
                }
            )
    return pd.DataFrame(rows)
