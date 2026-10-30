"""Event-level simulator of card-not-present payments on a shared platform.

The simulator returns one row per payment *attempt*. Columns are split into:

- public columns, known to the platform at decision time (``PUBLIC_COLUMNS``);
- feedback columns, which become known later (``label_observed_at``,
  ``observed_label``) and only for some attempts;
- private columns (``is_fraud``, ``fraud_type``), which exist only because this
  is a simulation. They must never be used as features or training labels for
  a deployable model; they are used for oracle comparisons and for evaluation.

Mechanisms that matter for fraud detection and are reproduced here:

- heterogeneous customers (spending scale, activity, favourite shops, devices);
- fraud campaigns with distinct modus operandi (card testing bursts followed by
  cash-out, direct cash-out, stealthy account takeover on the victim's device);
- adaptation: fraudsters progressively avoid the signal that the legacy rules
  rely on most (foreign IP addresses), creating concept drift;
- an already deployed rule-based policy that declines, reviews (with a daily
  analyst capacity) or approves each attempt *before* any label exists;
- delayed, incomplete and noisy feedback: reviews label within days,
  chargebacks arrive after weeks and only for a fraction of approved frauds,
  some legitimate payments are disputed as fraud ("friendly fraud"), and
  declined attempts never get a label (counterfactual censoring).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

COUNTRIES = np.array(["FR", "DE", "ES", "IT", "NL", "BE"])
COUNTRY_WEIGHTS = np.array([0.24, 0.27, 0.16, 0.17, 0.09, 0.07])
FOREIGN_EU = np.array(["PT", "PL", "AT", "IE"])
FOREIGN_NON_EU = np.array(["GB", "US", "RU", "NG", "BR"])
CATEGORIES = np.array(
    ["fashion", "electronics", "digital_goods", "travel", "grocery", "gaming", "marketplace", "home"]
)
CATEGORY_AMOUNT = np.array([1.3, 3.0, 0.5, 4.0, 1.0, 0.6, 1.2, 1.8])
CATEGORY_FRAUD_APPEAL = np.array([1.0, 2.5, 3.0, 1.5, 0.4, 2.5, 1.5, 0.7])
LEGIT_HOUR_WEIGHTS = np.array(
    [7, 4, 3, 3, 4, 8, 20, 40, 55, 60, 60, 60, 60, 65, 65, 65, 70, 75, 75, 70, 60, 45, 25, 14],
    dtype=float,
)
FRAUD_HOUR_WEIGHTS = np.array(
    [30, 30, 28, 25, 20, 18, 20, 30, 40, 45, 45, 45, 45, 45, 45, 45, 45, 45, 45, 45, 45, 42, 38, 34],
    dtype=float,
)

PUBLIC_COLUMNS = [
    "transaction_id",
    "timestamp",
    "customer_id",
    "customer_country",
    "account_age_days",
    "merchant_id",
    "merchant_category",
    "device_id",
    "device_age_days",
    "ip_country",
    "amount_eur",
    "legacy_score",
    "decision",
]
FEEDBACK_COLUMNS = ["label_observed_at", "observed_label", "label_source"]
PRIVATE_COLUMNS = ["is_fraud", "fraud_type"]


@dataclass(frozen=True)
class SimulationConfig:
    seed: int = 0
    start: str = "2025-01-06"
    n_days: int = 180
    n_customers: int = 6_000
    n_merchants: int = 40
    legit_per_day: float = 1_200.0
    campaigns_per_day: float = 0.7
    # Share of card-testing/cash-out attempts coming from a foreign IP address,
    # at the start and at the end of the simulated period (adaptive fraudsters).
    foreign_ip_start: float = 0.70
    foreign_ip_end: float = 0.25
    review_capacity_per_day: int = 20
    review_delay_days: float = 2.0
    chargeback_report_rate: float = 0.80
    chargeback_median_delay_days: float = 16.0
    friendly_fraud_rate: float = 0.001
    # Share of registered customers who never pay. Left at 0 so the small
    # teaching book (iterations 002–004) keeps its random stream.
    dormant_fraction: float = 0.0
    preexisting_age_min: float = 10.0
    preexisting_age_max: float = 2_000.0
    # "sequential" matches the original per-customer draw. "gumbel" is the
    # same weighted sample without replacement, vectorised for large books.
    favourite_sampling: str = "sequential"


def _rng_hours(rng, weights, n):
    return rng.choice(24, size=n, p=weights / weights.sum())


def mature_config() -> SimulationConfig:
    """A specialist European card-not-present book, not a 6,000-customer toy.

    One million registered customers, most of them quiet during the half-year
    window, about 8,000 attempts a day across 200 shops. The analyst queue
    grows from 20 to 50 reviews a day: operations do not scale with the book.
    Fraud campaigns are only modestly more frequent, so the attempt rate falls
    toward published card-not-present rates instead of staying at the teaching
    book's 0.43%.
    """
    return SimulationConfig(
        n_customers=1_000_000,
        n_merchants=200,
        legit_per_day=8_000,
        campaigns_per_day=1.2,
        review_capacity_per_day=50,
        dormant_fraction=0.85,
        preexisting_age_max=3_650,
        favourite_sampling="gumbel",
    )


def _gumbel_favourites(rng, n_customers: int, popularity, k: int = 4, chunk: int = 20_000) -> np.ndarray:
    """Weighted sample of ``k`` shops without replacement, in chunks."""
    log_p = np.log(np.asarray(popularity, dtype=float))
    out = np.empty((n_customers, k), dtype=np.int32)
    for start in range(0, n_customers, chunk):
        end = min(start + chunk, n_customers)
        scores = log_p + rng.gumbel(size=(end - start, log_p.size))
        out[start:end] = np.argpartition(-scores, kth=k - 1, axis=1)[:, :k]
    return out


def _make_entities(cfg: SimulationConfig, rng: np.random.Generator):
    start = pd.Timestamp(cfg.start, tz="UTC")
    id_width = max(5, len(str(cfg.n_customers - 1)))
    # Call order matches iterations 002–004 when dormant_fraction is 0.
    country = rng.choice(COUNTRIES, cfg.n_customers, p=COUNTRY_WEIGHTS)
    activity = rng.gamma(0.7, 1.0, cfg.n_customers)
    if cfg.dormant_fraction > 0:
        activity = np.where(rng.random(cfg.n_customers) < cfg.dormant_fraction, 0.0, activity)
    customers = pd.DataFrame(
        {
            "customer_id": [f"c{i:0{id_width}d}" for i in range(cfg.n_customers)],
            "country": country,
            "activity": activity,
            "amount_scale": rng.lognormal(np.log(35), 0.5, cfg.n_customers),
            # Most accounts pre-date the simulation, some are opened during it.
            "created_day": np.where(
                rng.random(cfg.n_customers) < 0.85,
                -rng.uniform(cfg.preexisting_age_min, cfg.preexisting_age_max, cfg.n_customers),
                rng.uniform(0, cfg.n_days, cfg.n_customers),
            ),
            "primary_device_age0": rng.gamma(2.0, 180.0, cfg.n_customers),
        }
    )
    cat_idx = rng.integers(0, len(CATEGORIES), cfg.n_merchants)
    merch_width = 2 if cfg.n_merchants < 100 else 4
    merchants = pd.DataFrame(
        {
            "merchant_id": [f"m{i:0{merch_width}d}" for i in range(cfg.n_merchants)],
            "category": CATEGORIES[cat_idx],
            "amount_mult": CATEGORY_AMOUNT[cat_idx],
            "popularity": rng.dirichlet(np.full(cfg.n_merchants, 1.5)),
            # Weak checkout security makes some shops much more attractive.
            "fraud_appeal": CATEGORY_FRAUD_APPEAL[cat_idx] * rng.lognormal(0, 0.8, cfg.n_merchants),
        }
    )
    if cfg.favourite_sampling == "sequential":
        favourites = np.stack(
            [rng.choice(cfg.n_merchants, 4, replace=False, p=merchants["popularity"]) for _ in range(cfg.n_customers)]
        )
    elif cfg.favourite_sampling == "gumbel":
        favourites = _gumbel_favourites(rng, cfg.n_customers, merchants["popularity"])
    else:
        raise ValueError(cfg.favourite_sampling)
    return start, customers, merchants, favourites


def _days_since(ts, start) -> np.ndarray:
    return np.asarray((pd.DatetimeIndex(ts) - start).total_seconds() / 86_400)


def _timestamps(rng, start, day, hour_weights):
    hours = _rng_hours(rng, hour_weights, len(day))
    seconds = hours * 3600 + rng.integers(0, 3600, len(day))
    return start + pd.to_timedelta(day, unit="D") + pd.to_timedelta(seconds, unit="s")


def _legit_attempts(cfg, rng, start, customers, merchants, favourites) -> pd.DataFrame:
    weekday_factor = np.array([1.0, 0.95, 0.95, 1.0, 1.1, 1.2, 1.15])
    day_weights = weekday_factor[(start.day_of_week + np.arange(cfg.n_days)) % 7]
    n = rng.poisson(cfg.legit_per_day * cfg.n_days)
    day = rng.choice(cfg.n_days, n, p=day_weights / day_weights.sum())
    cust = rng.choice(cfg.n_customers, n, p=customers["activity"] / customers["activity"].sum())
    ts = _timestamps(rng, start, day, LEGIT_HOUR_WEIGHTS)
    keep = _days_since(ts, start) > customers["created_day"].to_numpy()[cust]
    day, cust, ts = day[keep], cust[keep], ts[keep]
    n = len(cust)
    use_favourite = rng.random(n) < 0.7
    merch = np.where(
        use_favourite,
        favourites[cust, rng.integers(0, favourites.shape[1], n)],
        rng.choice(cfg.n_merchants, n, p=merchants["popularity"]),
    )
    amount = (
        customers["amount_scale"].to_numpy()[cust]
        * merchants["amount_mult"].to_numpy()[merch]
        * rng.lognormal(0, 0.7, n)
    )
    new_device = rng.random(n) < 0.05
    primary_age = customers["primary_device_age0"].to_numpy()[cust] + day
    home = customers["country"].to_numpy()[cust]
    travelling = rng.random(n) < 0.05
    abroad = np.where(rng.random(n) < 0.7, rng.choice(FOREIGN_EU, n), rng.choice(FOREIGN_NON_EU, n))
    return pd.DataFrame(
        {
            "timestamp": ts,
            "cust_idx": cust,
            "merch_idx": merch,
            "amount_eur": amount,
            "device_id": np.where(
                new_device,
                [f"d{c}_{k}" for c, k in zip(cust, rng.integers(1, 10**6, n))],
                [f"d{c}" for c in cust],
            ),
            "device_age_days": np.where(new_device, rng.exponential(3.0, n), primary_age),
            "ip_country": np.where(travelling, abroad, home),
            "is_fraud": False,
            "fraud_type": "none",
        }
    )


def _fraud_attempts(cfg, rng, start, customers, merchants) -> pd.DataFrame:
    n_campaigns = rng.poisson(cfg.campaigns_per_day * cfg.n_days)
    appeal = merchants["fraud_appeal"].to_numpy()
    digital = np.flatnonzero(merchants["category"].isin(["digital_goods", "gaming"]).to_numpy())
    parts = []
    for c in range(n_campaigns):
        day0 = rng.uniform(0, cfg.n_days - 1)
        progress = day0 / cfg.n_days
        p_foreign = cfg.foreign_ip_start + (cfg.foreign_ip_end - cfg.foreign_ip_start) * progress
        kind = rng.choice(["card_testing", "cash_out", "stealth"], p=[0.35, 0.45, 0.20])
        shops = rng.choice(cfg.n_merchants, rng.integers(1, 4), replace=False, p=appeal / appeal.sum())
        fraud_devices = [f"fd{c}_{k}" for k in range(rng.integers(1, 3))]
        foreign_ip = rng.random() < p_foreign
        ip = rng.choice(FOREIGN_NON_EU) if rng.random() < 0.6 else rng.choice(FOREIGN_EU)
        n_victims = int(rng.integers(1, 4))
        if cfg.dormant_fraction > 0:
            weights = customers["activity"].to_numpy()
            victims = rng.choice(cfg.n_customers, n_victims, replace=False, p=weights / weights.sum())
        else:
            victims = rng.choice(cfg.n_customers, n_victims, replace=False)
        for victim in victims:
            t0 = start + pd.Timedelta(days=day0) + pd.Timedelta(hours=int(_rng_hours(rng, FRAUD_HOUR_WEIGHTS, 1)[0]))
            home = customers["country"].iat[victim]
            scale = customers["amount_scale"].iat[victim]
            if kind == "card_testing":
                n_test, n_cash = rng.integers(2, 6), rng.integers(1, 3)
                offsets = np.concatenate(
                    [np.sort(rng.uniform(0, 0.5, n_test)), 0.5 + np.sort(rng.uniform(0, 6, n_cash))]
                )
                amounts = np.concatenate(
                    [rng.uniform(0.5, 5.0, n_test), rng.lognormal(np.log(220), 0.6, n_cash)]
                )
                merch = np.concatenate(
                    [np.full(n_test, rng.choice(digital) if len(digital) else shops[0]), rng.choice(shops, n_cash)]
                )
            elif kind == "cash_out":
                k = rng.integers(1, 5)
                offsets = np.sort(rng.uniform(0, 48, k))
                amounts = rng.lognormal(np.log(160), 0.7, k)
                merch = rng.choice(shops, k)
            else:
                k = rng.integers(1, 3)
                offsets = np.sort(rng.uniform(0, 24 * 7, k))
                amounts = scale * 2.0 * rng.lognormal(0, 0.5, k)
                merch = rng.choice(shops, k)
            k = len(offsets)
            stealth = kind == "stealth"
            # Some fraudsters spoof an old device fingerprint.
            spoofed = rng.random(k) < 0.25
            parts.append(
                pd.DataFrame(
                    {
                        "timestamp": t0 + pd.to_timedelta(offsets, unit="h"),
                        "cust_idx": victim,
                        "merch_idx": merch,
                        "amount_eur": amounts,
                        "device_id": f"d{victim}" if stealth else rng.choice(fraud_devices, k),
                        "device_age_days": (
                            customers["primary_device_age0"].iat[victim] + day0
                            if stealth
                            else np.where(spoofed, rng.gamma(2.0, 150.0, k), rng.exponential(1.5, k))
                        ),
                        "ip_country": ip if (foreign_ip and not stealth) else home,
                        "is_fraud": True,
                        "fraud_type": kind,
                    }
                )
            )
    return pd.concat(parts, ignore_index=True)


def _legacy_policy(cfg, rng, tx: pd.DataFrame) -> pd.DataFrame:
    """Hand-written rules deployed before any machine-learning model."""
    non_eu = tx["ip_country"].isin(FOREIGN_NON_EU).to_numpy()
    foreign = tx["ip_country"].ne(tx["customer_country"]).to_numpy()
    score = (
        1.6 * non_eu
        + 0.8 * (foreign & ~non_eu)
        + 1.2 * (tx["device_age_days"].to_numpy() < 1)
        + 0.6 * (tx["device_age_days"].to_numpy() < 7)
        + 0.9 * (tx["amount_eur"].to_numpy() > 400)
        + 0.5 * tx["merchant_category"].isin(["digital_goods", "gaming"]).to_numpy()
        + rng.normal(0, 0.5, len(tx))
    )
    tx["legacy_score"] = score.round(3)
    decision = np.where(score > 2.8, "declined", "approved").astype(object)
    # Analysts review the riskiest non-declined attempts, up to a daily capacity.
    candidates = (score > 1.5) & (decision == "approved")
    day = tx["timestamp"].dt.floor("D")
    rank = pd.Series(np.where(candidates, -score, np.inf)).groupby(day.to_numpy()).rank(method="first")
    reviewed = candidates & (rank.to_numpy() <= cfg.review_capacity_per_day)
    is_fraud = tx["is_fraud"].to_numpy()
    decision[reviewed & is_fraud] = "review_blocked"
    decision[reviewed & ~is_fraud] = "review_approved"
    tx["decision"] = decision
    return tx


def _feedback(cfg, rng, tx: pd.DataFrame) -> pd.DataFrame:
    n = len(tx)
    is_fraud = tx["is_fraud"].to_numpy()
    reviewed = tx["decision"].str.startswith("review").to_numpy()
    approved = tx["decision"].eq("approved").to_numpy()
    review_delay = pd.to_timedelta(cfg.review_delay_days + rng.exponential(1.0, n), unit="D")
    chargeback_delay = pd.to_timedelta(
        2 + rng.lognormal(np.log(cfg.chargeback_median_delay_days), 0.6, n), unit="D"
    )
    chargeback = approved & (
        (is_fraud & (rng.random(n) < cfg.chargeback_report_rate))
        | (~is_fraud & (rng.random(n) < cfg.friendly_fraud_rate))
    )
    observed_at = pd.Series(pd.NaT, index=tx.index, dtype="datetime64[ns, UTC]")
    observed_at[reviewed] = (tx["timestamp"] + review_delay)[reviewed]
    observed_at[chargeback] = (tx["timestamp"] + chargeback_delay)[chargeback]
    tx["label_observed_at"] = observed_at
    # Approved payments without a chargeback have no explicit label: the
    # platform only ever learns "no dispute so far".
    tx["observed_label"] = np.where(reviewed, is_fraud.astype(float), np.where(chargeback, 1.0, np.nan))
    tx["label_source"] = np.select([reviewed, chargeback], ["review", "chargeback"], "none")
    return tx


def simulate(cfg: SimulationConfig = SimulationConfig()) -> pd.DataFrame:
    rng = np.random.default_rng(cfg.seed)
    start, customers, merchants, favourites = _make_entities(cfg, rng)
    tx = pd.concat(
        [
            _legit_attempts(cfg, rng, start, customers, merchants, favourites),
            _fraud_attempts(cfg, rng, start, customers, merchants),
        ],
        ignore_index=True,
    )
    end = start + pd.Timedelta(days=cfg.n_days)
    tx = tx[tx["timestamp"] < end].sort_values("timestamp", kind="stable").reset_index(drop=True)
    tx["customer_id"] = customers["customer_id"].to_numpy()[tx["cust_idx"]]
    tx["customer_country"] = customers["country"].to_numpy()[tx["cust_idx"]]
    tx["account_age_days"] = (
        _days_since(tx["timestamp"], start) - customers["created_day"].to_numpy()[tx["cust_idx"]]
    ).clip(0).round(2)
    tx["merchant_id"] = merchants["merchant_id"].to_numpy()[tx["merch_idx"]]
    tx["merchant_category"] = merchants["category"].to_numpy()[tx["merch_idx"]]
    tx["amount_eur"] = tx["amount_eur"].clip(0.5, 5_000).round(2)
    tx["device_age_days"] = tx["device_age_days"].astype(float).round(2)
    tx["transaction_id"] = [f"t{i:07d}" for i in range(len(tx))]
    tx = _legacy_policy(cfg, rng, tx)
    tx = _feedback(cfg, rng, tx)
    return tx[PUBLIC_COLUMNS + FEEDBACK_COLUMNS + PRIVATE_COLUMNS]
