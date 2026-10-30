"""Iteration 002: is the v2 simulator a non-trivial learning problem?"""

import json
import time
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import average_precision_score, roc_auc_score

from fraud_sim.backtest import BacktestConfig, iter_folds
from fraud_sim.features import add_window_features
from fraud_sim.simulator import SimulationConfig, simulate

HERE = Path(__file__).parent
ROW = ["amount_eur", "device_age_days", "account_age_days", "ip_mismatch", "ip_non_eu", "hour"]
WINDOW = [
    "cust_n_1h", "cust_n_24h", "cust_amount_24h", "amount_to_cust_mean_30d", "cust_declined_24h",
    "cust_seconds_since_prev", "device_n_24h", "device_n_7d", "merchant_n_1h", "merchant_burst",
]

t0 = time.perf_counter()
tx = add_window_features(simulate(SimulationConfig()))
tx["hour"] = tx["timestamp"].dt.hour
t_sim = time.perf_counter() - t0

rows = []
for fold, (cutoff, cens, oracle, test, y_cens) in enumerate(iter_folds(tx, BacktestConfig())):
    y_test = tx.loc[test, "is_fraud"].to_numpy()
    rows.append(dict(fold=fold, model="legacy_score", features="-",
                     roc_auc=roc_auc_score(y_test, tx.loc[test, "legacy_score"]),
                     ap=average_precision_score(y_test, tx.loc[test, "legacy_score"])))
    for features_name, cols in (("row", ROW), ("row+window", ROW + WINDOW)):
        for labels, mask, y in (("censored", cens, y_cens[cens]), ("oracle", oracle, tx.loc[oracle, "is_fraud"])):
            model = HistGradientBoostingClassifier(random_state=0).fit(tx.loc[mask, cols], y.astype(int))
            p = model.predict_proba(tx.loc[test, cols])[:, 1]
            rows.append(dict(fold=fold, model=f"hgb_{labels}", features=features_name,
                             roc_auc=roc_auc_score(y_test, p), ap=average_precision_score(y_test, p)))

res = pd.DataFrame(rows)
summary = res.groupby(["model", "features"])[["roc_auc", "ap"]].agg(["mean", "std"]).round(3)
print(summary.to_string())
ap = tx["decision"].isin(["approved", "review_approved"])
stats = {
    "attempts": len(tx),
    "attempt_fraud_rate": float(tx["is_fraud"].mean()),
    "fraud_by_type": tx.loc[tx.is_fraud, "fraud_type"].value_counts().to_dict(),
    "realized_fraud_rate_count": float(tx.loc[ap, "is_fraud"].mean()),
    "realized_fraud_rate_value": float(tx.loc[ap & tx.is_fraud, "amount_eur"].sum() / tx.loc[ap, "amount_eur"].sum()),
    "decision_counts": tx["decision"].value_counts().to_dict(),
    "legacy_fraud_stopped_share": float(tx.loc[tx.is_fraud, "decision"].isin(["declined", "review_blocked"]).mean()),
    "simulate_and_features_seconds": round(t_sim, 2),
    "total_seconds": round(time.perf_counter() - t0, 2),
}
print(json.dumps(stats, indent=2))
res.to_csv(HERE / "fold_metrics.csv", index=False)
(HERE / "summary.json").write_text(json.dumps(stats, indent=2) + "\n")
summary.to_csv(HERE / "summary_metrics.csv")
