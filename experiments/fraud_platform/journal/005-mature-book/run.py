"""Iteration 005: the same backtest on a million-customer book."""

import json
import time
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

from fraud_sim.business import (
    APPROVE, Costs, decide, decide_on_top_of_legacy, legacy_actions, observable_labels, realised_gain,
)
from fraud_sim.evaluation import ranking_scorers
from fraud_sim.features import add_window_features
from fraud_sim.pipeline import backtest
from fraud_sim.simulator import mature_config, simulate

matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).parent
SMALL = HERE.parent / "004-business-evaluation" / "policy_summary.csv"
CFG = mature_config()
COSTS = Costs(review_capacity_per_day=CFG.review_capacity_per_day)
FEATURES = "row+window"

t0 = time.perf_counter()
log = simulate(CFG)
t_sim = time.perf_counter()
store = add_window_features(log)
t_feat = time.perf_counter()
active = int(log["customer_id"].nunique())
population = {
    "registered_customers": CFG.n_customers,
    "active_customers": active,
    "active_fraction": active / CFG.n_customers,
    "merchants": CFG.n_merchants,
    "attempts": len(log),
    "attempts_per_day": len(log) / CFG.n_days,
    "attempt_fraud_rate": float(log["is_fraud"].mean()),
    "daily_volume_eur": float(log["amount_eur"].sum() / CFG.n_days),
    "review_capacity_per_day": CFG.review_capacity_per_day,
    "median_account_age_days": float(log["account_age_days"].median()),
}
print(json.dumps(population, indent=2), flush=True)

metrics, preds = {}, {}
for labels in ("censored", "oracle"):
    t = time.perf_counter()
    metrics[labels], preds[labels] = backtest(
        store, FEATURES, labels, ranking_scorers(), return_predictions=True, cardinality_threshold=256,
    )
    print(labels, "fit_s", round(time.perf_counter() - t, 1), flush=True)
test = preds["censored"].drop(columns="p_fraud")
p_cens = preds["censored"]["p_fraud"].to_numpy()
p_orac = preds["oracle"]["p_fraud"].to_numpy()
is_fraud = test["is_fraud"].to_numpy()
amount = test["amount_eur"].to_numpy()
policies = {
    "legacy rules": legacy_actions(test),
    "censored model on top of legacy": decide_on_top_of_legacy(test, p_cens, COSTS),
    "censored model replaces legacy": decide(test, p_cens, COSTS),
    "oracle-label model replaces legacy": decide(test, p_orac, COSTS),
    "perfect clairvoyant": np.where(is_fraud, 1, APPROVE),
}
y_obs = observable_labels(test)
labelled = y_obs.notna().to_numpy()
rows = []
for name, action in policies.items():
    gain = realised_gain(action, is_fraud, amount, COSTS)
    naive = realised_gain(action[labelled], y_obs[labelled].to_numpy().astype(bool), amount[labelled], COSTS)
    for fold in range(int(test["fold"].max()) + 1):
        mask = test["fold"].to_numpy() == fold
        rows.append({
            "policy": name, "fold": fold,
            "gain_eur": float(gain[mask].sum()),
            "naive_gain_eur": float(naive[mask[labelled]].sum()),
            "volume_eur": float(amount[mask].sum()),
        })
res = pd.DataFrame(rows)
ref = res[res.policy == "legacy rules"].set_index("fold")
res["gain_vs_legacy"] = res["gain_eur"] - res["fold"].map(ref["gain_eur"])
res["naive_vs_legacy"] = res["naive_gain_eur"] - res["fold"].map(ref["naive_gain_eur"])
res.to_csv(HERE / "policy_folds.csv", index=False)
perfect = res.loc[res.policy == "perfect clairvoyant", "gain_vs_legacy"].sum()
summary = res.groupby("policy", sort=False).agg(
    gain_eur=("gain_eur", "sum"), gain_vs_legacy=("gain_vs_legacy", "sum"),
    gain_vs_legacy_min=("gain_vs_legacy", "min"), gain_vs_legacy_max=("gain_vs_legacy", "max"),
    naive_vs_legacy=("naive_vs_legacy", "sum"), volume_eur=("volume_eur", "sum"),
)
summary["share_of_perfect_uplift"] = summary["gain_vs_legacy"] / perfect
summary["uplift_per_million_eur"] = summary["gain_vs_legacy"] / summary["volume_eur"] * 1_000_000
print(summary.round(3).to_string())
summary.round(4).to_csv(HERE / "policy_summary.csv")
ranking = pd.concat(metrics.values()).groupby("labels")[["ap", "roc_auc", "calibration_ratio"]].agg(["mean", "std"])
print(ranking.round(3).to_string())
ranking.round(4).to_csv(HERE / "ranking.csv")

small = pd.read_csv(SMALL).set_index("policy")
order = ["censored model replaces legacy", "oracle-label model replaces legacy"]
fig, ax = plt.subplots(figsize=(7.2, 3.8))
x = np.arange(len(order))
for offset, frame, label in ((-0.18, small, "6,000-customer book"), (0.18, summary, "1,000,000-customer book")):
    values = [100 * frame.loc[name, "share_of_perfect_uplift"] for name in order]
    ax.bar(x + offset, values, width=0.36, label=label)
ax.set_xticks(x, ["Trained on censored\nhistory", "Trained on private\noracle labels"])
ax.set_ylabel("Share of the perfect uplift (%)")
ax.set_ylim(0, 100)
ax.set_title("Private labels add only a few points of uplift, on both books")
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig(HERE / "scale_uplift.svg")
fig.savefig(HERE / "scale_uplift.png", dpi=110)

info = {
    **population,
    "simulate_s": round(t_sim - t0, 1),
    "features_s": round(t_feat - t_sim, 1),
    "total_s": round(time.perf_counter() - t0, 1),
    "test_attempts": int(len(test)),
    "test_frauds": int(is_fraud.sum()),
}
(HERE / "run_info.json").write_text(json.dumps(info, indent=2) + "\n")
print(json.dumps(info, indent=2))
