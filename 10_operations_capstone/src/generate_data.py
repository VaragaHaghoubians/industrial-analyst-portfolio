"""One quarter of synthetic orders and production for the capstone story.

Night shifts lose more time. LATHE_01 scraps more Bracket pieces. Orders are
written from the same seed so the SQL gap is repeatable. This is practice
data, not a factory export.
"""

from pathlib import Path

import numpy as np
import pandas as pd

SEED = 42
DAYS = 90
START = pd.Timestamp("2025-01-06")
SHIFT_PLAN = {"Morning": 100, "Night": 80}
LINES = [
    ("PRESS_01", "Bracket"),
    ("WELD_01", "Housing"),
    ("LATHE_01", "Bracket"),
]


def build_tables(seed: int = SEED, days: int = DAYS) -> tuple[pd.DataFrame, pd.DataFrame]:
    rng = np.random.default_rng(seed)
    rows = []
    for day in range(days):
        date = START + pd.Timedelta(days=day)
        for shift, planned in SHIFT_PLAN.items():
            for machine, product in LINES:
                low, high = (8, 25) if shift == "Morning" else (25, 70)
                downtime = int(rng.integers(low, high))
                available = max(0.0, 1 - downtime / 450)
                actual = int(round(planned * available * float(rng.uniform(0.97, 1.03))))
                actual = min(planned, max(0, actual))
                scrap_rate = 0.055 if machine == "LATHE_01" else 0.015
                scrap = int(round(actual * scrap_rate))
                scrap = min(actual, scrap)
                if downtime >= 40:
                    reason = "Breakdown"
                elif downtime >= 20:
                    reason = "Setup"
                else:
                    reason = "Material wait"
                rows.append(
                    {
                        "date": date.strftime("%Y-%m-%d"),
                        "shift": shift,
                        "machine_id": machine,
                        "product": product,
                        "planned_qty": planned,
                        "actual_qty": actual,
                        "scrap_qty": scrap,
                        "downtime_min": downtime,
                        "reason": reason,
                    }
                )
    production = pd.DataFrame(rows)
    production["good_qty"] = production["actual_qty"] - production["scrap_qty"]
    weekly = production.copy()
    weekly["week_start"] = pd.to_datetime(weekly["date"]).dt.to_period("W-SUN").dt.start_time
    orders = []
    order_id = 1
    for (week_start, product), group in weekly.groupby(["week_start", "product"]):
        good = int(group["good_qty"].sum())
        factor = 1.08 if product == "Bracket" else 0.97
        orders.append(
            {
                "order_id": order_id,
                "week_start": pd.Timestamp(week_start).strftime("%Y-%m-%d"),
                "product": product,
                "order_qty": int(round(good * factor)),
            }
        )
        order_id += 1
    order_frame = pd.DataFrame(orders)
    return production.drop(columns=["good_qty"]), order_frame


def write_raw_data(root: Path, seed: int = SEED) -> tuple[pd.DataFrame, pd.DataFrame]:
    raw = root / "data" / "raw"
    raw.mkdir(parents=True, exist_ok=True)
    production, orders = build_tables(seed=seed)
    production.to_csv(raw / "production.csv", index=False)
    orders.to_csv(raw / "orders.csv", index=False)
    return production, orders
