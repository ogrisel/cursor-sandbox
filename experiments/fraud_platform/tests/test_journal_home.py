"""The rendered journal home page is the experiment's front door."""

import unittest
from pathlib import Path

INDEX = Path(__file__).resolve().parents[1] / "journal" / "index.md"


class JournalHomeTest(unittest.TestCase):
    def test_home_page_shows_highlight_plots_and_code_entry_points(self):
        text = INDEX.read_text()
        for plot in (
            "005-mature-book/scale_uplift.png",
            "003-skrub-dataops/leakage_ap.png",
            "004-business-evaluation/policy_uplift.png",
        ):
            self.assertIn(plot, text)
            self.assertTrue((INDEX.parent / plot).is_file(), plot)
        for entry in (
            "src/fraud_sim/simulator.py#L103-L122",
            "src/fraud_sim/simulator.py#L359-L383",
            "src/fraud_sim/features.py#L72-L91",
            "src/fraud_sim/features.py#L47-L69",
            "src/fraud_sim/backtest.py#L26-L43",
            "src/fraud_sim/pipeline.py#L85-L105",
            "src/fraud_sim/pipeline.py#L113-L145",
            "src/fraud_sim/business.py#L45-L62",
            "journal/005-mature-book/run.py",
        ):
            self.assertIn(entry, text)


if __name__ == "__main__":
    unittest.main()
