"""Iteration 003: skrub DataOps features, lag-aware label features, leakage."""

import json
import time
from pathlib import Path

import pandas as pd

from fraud_sim.evaluation import ranking_scorers
from fraud_sim.pipeline import backtest, feature_store_dataop
from fraud_sim.simulator import SimulationConfig, simulate

HERE = Path(__file__).parent
CONFIGS = [
    ("row", "censored"),
    ("row+window", "censored"),
    ("row+window+labels", "censored"),
    ("row+window+leaky_labels", "censored"),
    ("row+window+labels", "oracle"),
]

t0 = time.perf_counter()
log = simulate(SimulationConfig())
store = feature_store_dataop().skb.eval({"log": log})
timings = {"simulate_and_feature_store_s": round(time.perf_counter() - t0, 2)}

results = []
for feature_set, labels in CONFIGS:
    t = time.perf_counter()
    results.append(backtest(store, feature_set, labels, ranking_scorers()))
    timings[f"{feature_set}|{labels}_s"] = round(time.perf_counter() - t, 2)
res = pd.concat(results, ignore_index=True)
res.to_csv(HERE / "fold_metrics.csv", index=False)

metrics = ["ap", "ap_served", "roc_auc", "roc_auc_served", "brier", "calibration_ratio"]
summary = res.groupby(["labels", "feature_set"], sort=False)[metrics].agg(["mean", "std"]).round(3)
print(summary.to_string())
timings["total_s"] = round(time.perf_counter() - t0, 2)
print(json.dumps(timings, indent=2))
(HERE / "timings.json").write_text(json.dumps(timings, indent=2) + "\n")
summary.to_csv(HERE / "summary_metrics.csv")

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

res["config"] = res["labels"] + "\n" + res["feature_set"].str.replace("row+window", "rw", regex=False)
order = res["config"].unique()
fig, ax = plt.subplots(figsize=(8, 3.6))
for offset, column, label in ((-0.18, "ap", "backtest (features as computed offline)"),
                              (0.18, "ap_served", "served (features available at decision time)")):
    means = res.groupby("config", sort=False)[column].mean().reindex(order)
    ax.bar([i + offset for i in range(len(order))], means, width=0.36, label=label)
    ax.scatter([i + offset for i, c in enumerate(order) for _ in range(4)],
               [v for c in order for v in res.loc[res.config == c, column]], s=8, color="black", zorder=3)
ax.set_xticks(range(len(order)), order, fontsize=7)
ax.set_ylabel("Average precision on full test truth")
ax.set_title("Back-dated label features look good offline and fail once served")
ax.set_ylim(0, 1.0)
ax.legend(fontsize=7, loc="upper left", ncols=2)
fig.tight_layout()
fig.savefig(HERE / "leakage_ap.svg")
fig.savefig(HERE / "leakage_ap.png", dpi=110)
