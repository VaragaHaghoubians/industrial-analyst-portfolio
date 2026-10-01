"""Checks that SQL, pandas and the statistical test agree."""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cleaning import clean_tables
from generate_data import build_tables
from kpi import add_measures
from sql_questions import run_questions
from shift_stats import compare_shifts, scrap_rate_interval


class CapstoneTests(unittest.TestCase):
    def setUp(self):
        self.production, self.orders = clean_tables(*build_tables())

    def test_sql_good_units_match_pandas(self):
        answers = run_questions(self.production, self.orders)
        pandas_good = (
            add_measures(self.production).groupby("product")["good_qty"].sum().sort_index()
        )
        sql_good = answers["good_units_by_product"].set_index("product")["good_qty"].sort_index()
        self.assertTrue(pandas_good.astype(int).equals(sql_good.astype(int)))

    def test_attainment_is_actual_over_planned(self):
        answers = run_questions(self.production, self.orders)
        morning = self.production.loc[self.production["shift"] == "Morning"]
        expected = morning["actual_qty"].sum() / morning["planned_qty"].sum()
        got = float(
            answers["attainment_by_shift"].set_index("shift").loc["Morning", "attainment"]
        )
        self.assertAlmostEqual(got, expected, places=4)

    def test_shift_test_and_scrap_interval_are_probabilities(self):
        comparison = compare_shifts(self.production)
        interval = scrap_rate_interval(self.production)
        self.assertGreater(comparison["morning_mean_good"], comparison["night_mean_good"])
        self.assertGreaterEqual(comparison["p_value"], 0)
        self.assertLessEqual(comparison["p_value"], 1)
        self.assertLess(interval["low"], interval["mean_daily_scrap_rate"])
        self.assertGreater(interval["high"], interval["mean_daily_scrap_rate"])


if __name__ == "__main__":
    unittest.main()
