"""Iteration 004: business value of policies, evaluation bias, calibration."""

import json
import time
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

from fraud_sim.business import (
    APPROVE, DECLINE, REVIEW, Costs, decide, decide_on_top_of_legacy, legacy_actions,
    observable_labels, realised_gain,
)
from fraud_sim.evaluation import ranking_scorers
from fraud_sim.pipeline import backtest, feature_store_dataop
from fraud_sim.simulator import SimulationConfig, simulate

matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).parent
COSTS = Costs()
FEATURES = "row+window"

t0 = time.perf_counter()
log = simulate(SimulationConfig())
# Local inspection copy. Gitignored so the report publisher does not check it out.
log.to_parquet(HERE / "transactions.parquet", index=False, compression="zstd")
store = feature_store_dataop().skb.eval({"log": log})
metrics, preds = {}, {}
for labels in ("censored", "oracle"):
    metrics[labels], preds[labels] = backtest(store, FEATURES, labels, ranking_scorers(), return_predictions=True)
test = preds["censored"].drop(columns="p_fraud")
assert (preds["oracle"]["transaction_id"] == test["transaction_id"]).all()
p_cens, p_orac = preds["censored"]["p_fraud"].to_numpy(), preds["oracle"]["p_fraud"].to_numpy()
is_fraud, amount = test["is_fraud"].to_numpy(), test["amount_eur"].to_numpy()

policies = {
    "approve all": np.full(len(test), APPROVE),
    "legacy rules": legacy_actions(test),
    "censored model on top of legacy": decide_on_top_of_legacy(test, p_cens, COSTS),
    "censored model replaces legacy": decide(test, p_cens, COSTS),
    "oracle-label model replaces legacy": decide(test, p_orac, COSTS),
    "perfect clairvoyant": np.where(is_fraud, DECLINE, APPROVE),
}

rows = []
y_obs = observable_labels(test)
labelled = y_obs.notna().to_numpy()
for name, action in policies.items():
    gain = realised_gain(action, is_fraud, amount, COSTS)
    naive = realised_gain(action[labelled], y_obs[labelled].to_numpy().astype(bool), amount[labelled], COSTS)
    for fold in range(test["fold"].max() + 1):
        f = test["fold"].to_numpy() == fold
        stopped = (action != APPROVE) & is_fraud & f
        rows.append({
            "policy": name, "fold": fold,
            "gain_eur": gain[f].sum(),
            "naive_gain_eur": naive[f[labelled]].sum(),
            "fraud_loss_eur": -gain[f & is_fraud & (action == APPROVE)].sum(),
            "fraud_stopped_share": stopped.sum() / (is_fraud & f).sum(),
            "fraud_value_stopped_share": amount[stopped].sum() / amount[is_fraud & f].sum(),
            "legit_declined": int(((action == DECLINE) & ~is_fraud & f).sum()),
            "reviews": int(((action == REVIEW) & f).sum()),
            **{f"stopped_{k}": ((action != APPROVE) & f & (test["fraud_type"] == k)).sum()
               / max(1, (f & (test["fraud_type"] == k)).sum())
               for k in ("card_testing", "cash_out", "stealth")},
        })
res = pd.DataFrame(rows)
res.to_csv(HERE / "policy_fold_metrics.csv", index=False)

ref = res[res.policy == "legacy rules"].set_index("fold")
res["gain_vs_legacy"] = res["gain_eur"] - res["fold"].map(ref["gain_eur"])
res["naive_gain_vs_legacy"] = res["naive_gain_eur"] - res["fold"].map(ref["naive_gain_eur"])
summary = res.groupby("policy", sort=False).agg(
    gain_eur=("gain_eur", "sum"),
    gain_vs_legacy=("gain_vs_legacy", "sum"),
    gain_vs_legacy_min_fold=("gain_vs_legacy", "min"),
    gain_vs_legacy_max_fold=("gain_vs_legacy", "max"),
    naive_gain_vs_legacy=("naive_gain_vs_legacy", "sum"),
    fraud_loss_eur=("fraud_loss_eur", "sum"),
    fraud_value_stopped_share=("fraud_value_stopped_share", "mean"),
    legit_declined=("legit_declined", "sum"),
    reviews=("reviews", "sum"),
    stopped_card_testing=("stopped_card_testing", "mean"),
    stopped_cash_out=("stopped_cash_out", "mean"),
    stopped_stealth=("stopped_stealth", "mean"),
)
perfect = summary.loc["perfect clairvoyant", "gain_vs_legacy"]
summary["share_of_perfect_uplift"] = summary["gain_vs_legacy"] / perfect
print(summary.round(3).to_string())
summary.round(4).to_csv(HERE / "policy_summary.csv")

scales = np.logspace(-2, 2, 17)
sweep = pd.DataFrame({
    "threshold_scale": scales,
    **{name: [realised_gain(decide(test, p, COSTS, s), is_fraud, amount, COSTS).sum() for s in scales]
       for name, p in (("censored", p_cens), ("oracle", p_orac))},
})
sweep.to_csv(HERE / "threshold_sweep.csv", index=False)
print(sweep.round(0).to_string())

ranking = pd.concat(metrics.values()).groupby("labels")[["ap", "roc_auc", "brier", "calibration_ratio"]].mean()
print(ranking.round(3).to_string())
ranking.round(4).to_csv(HERE / "ranking_metrics.csv")
timing = {"total_s": round(time.perf_counter() - t0, 2), "test_rows": len(test), "test_frauds": int(is_fraud.sum())}
(HERE / "run_info.json").write_text(json.dumps(timing, indent=2) + "\n")
print(timing)

fig, ax = plt.subplots(figsize=(8, 3.8))
order = [p for p in policies if p != "approve all"]
per_fold = res.set_index("policy").loc[order]
for i, name in enumerate(order):
    values = per_fold.loc[name, "gain_vs_legacy"]
    ax.bar(i, values.mean(), color="tab:blue" if "censored" in name else "tab:gray")
    ax.scatter(np.full(len(values), i), values, color="black", s=10, zorder=3)
ax.axhline(0, color="black", lw=0.8)
ax.set_xticks(range(len(order)), [n.replace(" model", "\nmodel").replace(" replaces", "\nreplaces") for n in order],
              fontsize=7)
ax.set_ylabel("Gain vs legacy per 21-day window (EUR)")
ax.set_title("Business uplift over the legacy rules (bars: mean, dots: folds)")
fig.tight_layout()
fig.savefig(HERE / "policy_uplift.svg")
fig.savefig(HERE / "policy_uplift.png", dpi=110)

fig, ax = plt.subplots(figsize=(6, 3.6))
legacy_total = summary.loc["legacy rules", "gain_eur"]
for name in ("censored", "oracle"):
    ax.plot(sweep["threshold_scale"], sweep[name] - legacy_total, marker="o", ms=3, label=f"{name}-label model")
ax.axvline(1, color="black", lw=0.8, ls="--")
ax.axhline(0, color="gray", lw=0.8)
ax.set_xscale("log")
ax.set_ylim(-20_000, 1.3 * (sweep[["censored", "oracle"]].max().max() - legacy_total))
ax.set_xlabel("Odds multiplier applied to predicted fraud probability")
ax.set_ylabel("Total gain vs legacy (EUR, 4 folds)")
ax.set_title("Is the Bayes threshold well placed? (1 = trust probabilities)")
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig(HERE / "threshold_sweep.svg")
fig.savefig(HERE / "threshold_sweep.png", dpi=110)
