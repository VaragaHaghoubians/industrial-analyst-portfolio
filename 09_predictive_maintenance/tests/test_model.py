"""Checks that the rare class is real and the baseline misses it."""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cleaning import FEATURES, clean_readings
from generate_data import machine_days
from model import train_and_compare


class MaintenanceModelTests(unittest.TestCase):
    def test_failures_are_uncommon_and_not_used_as_inputs(self):
        frame = clean_readings(machine_days())
        self.assertGreater(frame["failure"].mean(), 0.02)
        self.assertLess(frame["failure"].mean(), 0.15)
        self.assertNotIn("failure", FEATURES)

    def test_balanced_model_finds_failures_the_baseline_misses(self):
        result = train_and_compare(clean_readings(machine_days()))
        self.assertEqual(result["baseline"]["recall"], 0.0)
        self.assertGreater(result["model"]["recall"], result["baseline"]["recall"])
        self.assertGreater(result["test_failures"], 0)
        matrix = result["model"]["confusion_matrix"]
        self.assertEqual(len(matrix), 2)
        self.assertEqual(len(matrix[0]), 2)


if __name__ == "__main__":
    unittest.main()
