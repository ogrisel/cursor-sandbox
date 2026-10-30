import unittest

import numpy as np
import pandas as pd

from fraud_sim.backtest import label_as_known_at
from fraud_sim.features import arrived_label_count, rolling_by_key
from fraud_sim.simulator import PRIVATE_COLUMNS, PUBLIC_COLUMNS, SimulationConfig, mature_config, simulate

T0 = pd.Timestamp("2025-01-01T12:00:00Z")


def _log(**columns):
    n = len(columns["minutes"])
    base = {
        "timestamp": T0 + pd.to_timedelta(columns.pop("minutes"), unit="min"),
        "customer_id": ["c1"] * n,
        "merchant_id": ["m1"] * n,
        "amount_eur": [10.0] * n,
        "observed_label": [np.nan] * n,
        "label_observed_at": pd.Series([pd.NaT] * n, dtype="datetime64[ns, UTC]"),
        "decision": ["approved"] * n,
    }
    base.update(columns)
    return pd.DataFrame(base)


class WindowTest(unittest.TestCase):
    def test_window_excludes_current_and_future_rows(self):
        tx = _log(minutes=[0, 30, 90, 60 * 30], amount_eur=[1.0, 2.0, 4.0, 8.0])
        # Windows are [t - 1h, t): minute 90 sees minute 30, never itself.
        np.testing.assert_array_equal(rolling_by_key(tx, "customer_id", "1h"), [0, 1, 1, 0])
        np.testing.assert_array_equal(rolling_by_key(tx, "customer_id", "24h", agg="sum"), [0, 1, 3, 0])

    def test_rolling_is_aligned_with_unsorted_keys(self):
        tx = _log(minutes=[0, 1, 2, 3], customer_id=["b", "a", "b", "a"])
        np.testing.assert_array_equal(rolling_by_key(tx, "customer_id", "1h"), [0, 0, 1, 1])


class LabelLagTest(unittest.TestCase):
    def test_label_only_counts_after_arrival(self):
        tx = _log(
            minutes=[0, 60, 60 * 24 * 10],
            observed_label=[1.0, np.nan, np.nan],
            label_observed_at=pd.Series([T0 + pd.Timedelta(days=5), pd.NaT, pd.NaT], dtype="datetime64[ns, UTC]"),
        )
        week = pd.Timedelta(days=30)
        np.testing.assert_array_equal(arrived_label_count(tx, "merchant_id", week), [0, 0, 1])
        np.testing.assert_array_equal(arrived_label_count(tx, "merchant_id", week, by="timestamp"), [0, 1, 1])

    def test_censoring_rules(self):
        cutoff = T0 + pd.Timedelta(days=60)
        tx = _log(
            minutes=[0, 0, 0, 60 * 24 * 50],
            decision=["declined", "approved", "approved", "approved"],
            observed_label=[np.nan, 1.0, np.nan, np.nan],
            label_observed_at=pd.Series([pd.NaT, cutoff + pd.Timedelta(days=1), pd.NaT, pd.NaT],
                                        dtype="datetime64[ns, UTC]"),
        )
        label = label_as_known_at(tx, cutoff, maturity_days=45)
        # Declined: never labelled. Late chargeback: still looks legitimate.
        # Recent approved: not yet mature.
        np.testing.assert_array_equal(label.to_numpy(), [np.nan, 0.0, 0.0, np.nan])


class SimulatorTest(unittest.TestCase):
    def test_small_run_is_deterministic_and_well_formed(self):
        cfg = SimulationConfig(n_days=20, n_customers=500, legit_per_day=200, campaigns_per_day=2)
        a, b = simulate(cfg), simulate(cfg)
        pd.testing.assert_frame_equal(a, b)
        self.assertEqual(list(a.columns[: len(PUBLIC_COLUMNS)]), PUBLIC_COLUMNS)
        self.assertTrue(set(PRIVATE_COLUMNS) <= set(a.columns))
        self.assertTrue(a["timestamp"].is_monotonic_increasing)
        self.assertTrue(a.loc[a.decision.eq("declined"), "observed_label"].isna().all())
        arrived = a["label_observed_at"].notna()
        self.assertTrue((a.loc[arrived, "label_observed_at"] > a.loc[arrived, "timestamp"]).all())

    def test_mature_book_keeps_most_customers_quiet(self):
        cfg = mature_config()
        self.assertGreaterEqual(cfg.n_customers, 100_000)
        self.assertGreater(cfg.dormant_fraction, 0.5)
        common = dict(n_days=15, n_customers=400, n_merchants=120, legit_per_day=120,
                      campaigns_per_day=0.3, favourite_sampling="gumbel")
        quiet = simulate(SimulationConfig(dormant_fraction=0.85, **common))
        busy = simulate(SimulationConfig(**common))
        self.assertLess(quiet["customer_id"].nunique(), 150)
        self.assertGreater(busy["customer_id"].nunique(), 250)
        self.assertTrue(quiet["merchant_id"].str.fullmatch(r"m\d{4}").all())


if __name__ == "__main__":
    unittest.main()
