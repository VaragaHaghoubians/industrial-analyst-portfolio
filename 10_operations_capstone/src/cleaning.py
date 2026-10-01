"""Checks the capstone tables before SQL and statistics."""

import pandas as pd


def clean_tables(production: pd.DataFrame, orders: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    production = production.copy()
    orders = orders.copy()
    production["date"] = pd.to_datetime(production["date"])
    orders["week_start"] = pd.to_datetime(orders["week_start"])
    for column in ("planned_qty", "actual_qty", "scrap_qty", "downtime_min"):
        production[column] = production[column].astype(int)
    orders["order_qty"] = orders["order_qty"].astype(int)
    if production.duplicated(["date", "shift", "machine_id"]).any():
        raise ValueError("Each machine can have only one row per shift.")
    if (production["actual_qty"] > production["planned_qty"]).any():
        raise ValueError("Actual quantity cannot exceed the plan.")
    if (production["scrap_qty"] > production["actual_qty"]).any():
        raise ValueError("Scrap cannot exceed actual quantity.")
    if (production[["planned_qty", "actual_qty", "scrap_qty", "downtime_min"]] < 0).any().any():
        raise ValueError("Quantities and downtime cannot be negative.")
    if (production["planned_qty"] == 0).any():
        raise ValueError("Planned quantity must be positive so attainment is defined.")
    if orders["order_id"].duplicated().any():
        raise ValueError("Order ids must be unique.")
    return production, orders
