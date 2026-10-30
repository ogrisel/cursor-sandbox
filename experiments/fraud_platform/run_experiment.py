"""Generate a simulated platform history and run the censored-label backtest."""

from __future__ import annotations

import json
from pathlib import Path

from workspace.fraud_platform import SimulationConfig, evaluate_backtest, simulate


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "journal" / "001-simulator" / "data"


def main() -> None:
    DATA.mkdir(exist_ok=True)
    transactions = simulate(SimulationConfig())
    # This represents the platform's internal event log. Consumers must remove
    # is_fraud before modelling; it is retained solely for simulator evaluation.
    transactions.to_csv(DATA / "transactions.csv.gz", index=False, compression="gzip")
    results = evaluate_backtest(transactions)
    results.to_csv(DATA / "backtest_results.csv", index=False)
    summary = {
        "attempts": len(transactions),
        "attempt_fraud_rate": float(transactions["is_fraud"].mean()),
        "declined_fraction": float(transactions["decision"].eq("declined").mean()),
        "labelled_fraction": float(transactions["observed_fraud_label"].notna().mean()),
        "reported_label_fraction": float(
            transactions.loc[transactions["decision"].eq("approved"), "observed_fraud_label"].notna().mean()
        ),
        "backtest": results.to_dict(orient="records"),
    }
    (DATA / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
