import unittest

import numpy as np
import pandas as pd

from fraud_sim.business import APPROVE, DECLINE, REVIEW, Costs, decide, observable_labels, realised_gain

T0 = pd.Timestamp("2025-01-01T12:00:00Z")


class BusinessTest(unittest.TestCase):
    def test_gain_matrix(self):
        c = Costs()
        action = np.array([APPROVE, APPROVE, DECLINE, DECLINE, REVIEW, REVIEW])
        fraud = np.array([False, True, False, True, False, True])
        gain = realised_gain(action, fraud, np.full(6, 100.0), c)
        np.testing.assert_allclose(gain, [2.0, -120.0, -10.0, 0.0, -3.0, -5.0])

    def test_decisions_follow_expected_gain_and_review_capacity(self):
        c = Costs(review_capacity_per_day=1)
        tx = pd.DataFrame({"timestamp": [T0] * 4, "amount_eur": [50.0, 50.0, 1000.0, 1000.0]})
        # Low risk approved; high risk declined; ambiguous big tickets compete for one review slot.
        action = decide(tx, np.array([0.001, 0.9, 0.05, 0.2]), c)
        np.testing.assert_array_equal(action, [APPROVE, DECLINE, REVIEW, DECLINE])

    def test_observable_labels_hide_declines_and_unreported_fraud(self):
        tx = pd.DataFrame({
            "decision": ["declined", "approved", "approved", "review_blocked"],
            "is_fraud": [True, True, False, True],
            "observed_label": [np.nan, np.nan, 1.0, 1.0],
        })
        np.testing.assert_array_equal(observable_labels(tx).to_numpy(), [np.nan, 0.0, 1.0, 1.0])


if __name__ == "__main__":
    unittest.main()
