"""Synthetic spare-part and finished-good demand for an inventory policy.

The numbers are generated with a fixed seed. They are practice data, not a
real warehouse extract.
"""

from pathlib import Path

import numpy as np
import pandas as pd

SEED = 42
WEEKS = 52
FIRST_MONDAY = pd.Timestamp("2025-01-06")

# sku, category, unit_cost, order_cost, holding_rate, lead_time_weeks,
# service_level, on_hand, mean_weekly, sigma_weekly
SKUS = [
    ("BRACKET", "finished good", 8.0, 75.0, 0.22, 2, 0.95, 450, 160, 28),
    ("HOUSING", "finished good", 22.0, 90.0, 0.22, 3, 0.95, 280, 70, 14),
    ("SUPPORT", "finished good", 15.0, 80.0, 0.22, 2, 0.95, 520, 40, 8),
    ("BEARING", "spare part", 45.0, 60.0, 0.25, 4, 0.98, 10, 6, 3),
    ("FILTER", "spare part", 18.0, 40.0, 0.25, 2, 0.95, 50, 10, 4),
    ("SEAL-KIT", "spare part", 30.0, 50.0, 0.25, 3, 0.97, 6, 4, 2),
    ("WELD-TIP", "spare part", 6.0, 35.0, 0.20, 1, 0.95, 80, 25, 6),
    ("HYDRAULIC-HOSE", "spare part", 120.0, 110.0, 0.18, 6, 0.99, 3, 2, 1.2),
]


def sku_master() -> pd.DataFrame:
    columns = [
        "sku",
        "category",
        "unit_cost",
        "order_cost",
        "holding_rate",
        "lead_time_weeks",
        "service_level",
        "on_hand",
    ]
    rows = [row[:8] for row in SKUS]
    return pd.DataFrame(rows, columns=columns)


def weekly_demand(seed: int = SEED, weeks: int = WEEKS) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []
    for sku, *_rest, mean_weekly, sigma_weekly in SKUS:
        draws = rng.normal(mean_weekly, sigma_weekly, size=weeks)
        demand = np.clip(np.rint(draws), 0, None).astype(int)
        for week, units in enumerate(demand, start=1):
            rows.append(
                {
                    "sku": sku,
                    "week": week,
                    "week_start": FIRST_MONDAY + pd.Timedelta(days=7 * (week - 1)),
                    "demand_units": int(units),
                }
            )
    return pd.DataFrame(rows)


def write_raw_data(root: Path, seed: int = SEED) -> tuple[pd.DataFrame, pd.DataFrame]:
    raw = root / "data" / "raw"
    raw.mkdir(parents=True, exist_ok=True)
    master = sku_master()
    weekly = weekly_demand(seed=seed)
    master.to_csv(raw / "sku_master.csv", index=False)
    weekly.to_csv(raw / "weekly_demand.csv", index=False)
    return weekly, master
