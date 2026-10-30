"""Regression checks for the causal transaction feature store."""

from __future__ import annotations

import unittest

import pandas as pd

from workspace.fraud_platform import add_causal_features


class CausalFeaturesTest(unittest.TestCase):
    def test_current_and_future_rows_do_not_enter_history(self):
        timestamp = pd.Timestamp("2025-01-01T12:00:00Z")
        raw = pd.DataFrame(
            {
                "timestamp": [timestamp, timestamp + pd.Timedelta(minutes=30), timestamp + pd.Timedelta(days=2)],
                "customer_id": ["c1", "c1", "c1"],
                "merchant_id": ["m1", "m1", "m1"],
                "device_id": ["d1", "d1", "d1"],
                "amount_eur": [20.0, 30.0, 40.0],
            }
        )
        featured = add_causal_features(raw)
        self.assertEqual(featured["customer_attempts_1d"].tolist(), [0.0, 1.0, 0.0])
        self.assertEqual(featured["merchant_attempts_1h"].tolist(), [0.0, 1.0, 0.0])
        self.assertEqual(featured["customer_amount_7d"].tolist(), [0.0, 20.0, 50.0])


if __name__ == "__main__":
    unittest.main()
