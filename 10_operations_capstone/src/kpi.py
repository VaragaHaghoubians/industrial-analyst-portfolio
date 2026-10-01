"""Pandas versions of the operations measures."""

import pandas as pd


def add_measures(production: pd.DataFrame) -> pd.DataFrame:
    frame = production.copy()
    frame["good_qty"] = frame["actual_qty"] - frame["scrap_qty"]
    frame["attainment"] = frame["actual_qty"] / frame["planned_qty"]
    frame["scrap_rate"] = frame["scrap_qty"] / frame["actual_qty"].where(frame["actual_qty"] > 0)
    return frame


def shift_summary(production: pd.DataFrame) -> pd.DataFrame:
    frame = add_measures(production)
    grouped = frame.groupby("shift", as_index=False).agg(
        planned_qty=("planned_qty", "sum"),
        actual_qty=("actual_qty", "sum"),
        good_qty=("good_qty", "sum"),
        scrap_qty=("scrap_qty", "sum"),
        downtime_min=("downtime_min", "sum"),
    )
    grouped["attainment"] = grouped["actual_qty"] / grouped["planned_qty"]
    grouped["scrap_rate"] = grouped["scrap_qty"] / grouped["actual_qty"]
    return grouped


def daily_good_units(production: pd.DataFrame) -> pd.DataFrame:
    frame = add_measures(production)
    return (
        frame.groupby(["date", "shift"], as_index=False)["good_qty"]
        .sum()
        .sort_values(["date", "shift"])
    )


def dashboard_table(production: pd.DataFrame) -> pd.DataFrame:
    frame = add_measures(production)
    frame["date"] = pd.to_datetime(frame["date"]).dt.strftime("%Y-%m-%d")
    return frame[
        [
            "date",
            "shift",
            "machine_id",
            "product",
            "planned_qty",
            "actual_qty",
            "good_qty",
            "scrap_qty",
            "downtime_min",
            "reason",
        ]
    ]
