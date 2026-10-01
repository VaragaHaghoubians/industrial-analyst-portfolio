"""Checks before the inventory formulas run."""

import pandas as pd


def clean_inputs(weekly: pd.DataFrame, master: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    weekly = weekly.copy()
    master = master.copy()
    weekly["week"] = weekly["week"].astype(int)
    weekly["demand_units"] = weekly["demand_units"].astype(int)
    weekly["week_start"] = pd.to_datetime(weekly["week_start"])
    master["lead_time_weeks"] = master["lead_time_weeks"].astype(int)
    master["on_hand"] = master["on_hand"].astype(int)

    if weekly.duplicated(["sku", "week"]).any():
        raise ValueError("Each SKU can appear only once in a week.")
    if (weekly["demand_units"] < 0).any():
        raise ValueError("Demand cannot be negative.")
    if master["sku"].duplicated().any():
        raise ValueError("SKU master has duplicate codes.")
    missing = set(master["sku"]) - set(weekly["sku"])
    extra = set(weekly["sku"]) - set(master["sku"])
    if missing or extra:
        raise ValueError("SKU master and weekly demand do not list the same SKUs.")
    if (master["unit_cost"] <= 0).any() or (master["order_cost"] <= 0).any():
        raise ValueError("Unit cost and order cost must be positive.")
    if ((master["holding_rate"] <= 0) | (master["holding_rate"] >= 1)).any():
        raise ValueError("Holding rate must be a fraction between 0 and 1.")
    if ((master["service_level"] <= 0.5) | (master["service_level"] >= 1)).any():
        raise ValueError("Service level must be between 0.5 and 1.")
    if (master["lead_time_weeks"] <= 0).any():
        raise ValueError("Lead time must be at least one week.")
    if (master["on_hand"] < 0).any():
        raise ValueError("On-hand stock cannot be negative.")
    return weekly, master
