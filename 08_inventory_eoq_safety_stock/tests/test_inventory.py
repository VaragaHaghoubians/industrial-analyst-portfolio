"""Checks for the EOQ and safety-stock formulas."""

import math
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from generate_data import sku_master, weekly_demand
from inventory import (
    build_policy,
    economic_order_quantity,
    order_policy_cost,
    safety_stock,
    z_score,
)


class InventoryFormulaTests(unittest.TestCase):
    def test_classic_eoq_square_root(self):
        # EOQ = sqrt(2 * 1000 * 50 / 2) = sqrt(50000)
        quantity = economic_order_quantity(1000, 50, 2)
        self.assertAlmostEqual(quantity, math.sqrt(50000), places=6)

    def test_order_and_hold_costs_meet_at_the_eoq(self):
        quantity = economic_order_quantity(1000, 50, 2)
        costs = order_policy_cost(1000, 50, 2, quantity)
        self.assertAlmostEqual(costs["ordering_cost"], costs["holding_cost"], places=6)

    def test_safety_stock_grows_with_lead_time(self):
        short = safety_stock(10, 1, 0.95)
        long = safety_stock(10, 4, 0.95)
        self.assertAlmostEqual(long, short * 2, places=6)
        self.assertAlmostEqual(z_score(0.95), 1.64485362695, places=5)

    def test_policy_flags_are_consistent_with_the_reorder_point(self):
        policy = build_policy(weekly_demand(), sku_master())
        self.assertEqual(len(policy), 8)
        for row in policy.itertuples(index=False):
            if row.action == "Reorder now":
                self.assertLessEqual(row.on_hand, row.reorder_point)
            if row.action == "Inside the band":
                self.assertGreater(row.on_hand, row.reorder_point)


if __name__ == "__main__":
    unittest.main()
