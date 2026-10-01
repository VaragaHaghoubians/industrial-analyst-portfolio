"""Checks before the failure model is trained."""

import pandas as pd

FEATURES = [
    "vibration_mm_s",
    "temperature_c",
    "pressure_bar",
    "hours_since_maintenance",
]


def clean_readings(frame: pd.DataFrame) -> pd.DataFrame:
    clean = frame.copy()
    clean["date"] = pd.to_datetime(clean["date"])
    clean["failure"] = clean["failure"].astype(int)
    if clean.duplicated(["date", "machine_id"]).any():
        raise ValueError("Each machine can have only one row per day.")
    if not set(clean["failure"]).issubset({0, 1}):
        raise ValueError("Failure must be 0 or 1.")
    if clean[FEATURES + ["runtime_hours"]].isna().any().any():
        raise ValueError("Sensor readings cannot be missing.")
    if (clean[FEATURES + ["runtime_hours"]] < 0).any().any():
        raise ValueError("Sensor readings cannot be negative.")
    return clean.sort_values(["date", "machine_id"]).reset_index(drop=True)
