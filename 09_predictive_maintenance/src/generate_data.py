"""Synthetic daily machine readings with a rare failure label.

A failure is more likely when vibration, temperature and hours since
maintenance are high. The label is created after the readings, so those
readings are allowed as model inputs. This is practice data, not a plant
historian export.
"""

from pathlib import Path

import numpy as np
import pandas as pd

SEED = 42
DAYS = 180
START = pd.Timestamp("2025-01-01")
MACHINES = ["PRESS_01", "WELD_01", "LATHE_01", "PACK_01"]


def _failure_probability(vibration: np.ndarray, temperature: np.ndarray, hours: np.ndarray) -> np.ndarray:
    score = -4.4 + 0.55 * (vibration - 3.0) + 0.08 * (temperature - 65.0) + 0.03 * hours
    return 1 / (1 + np.exp(-score))


def machine_days(seed: int = SEED, days: int = DAYS) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []
    for machine_index, machine in enumerate(MACHINES):
        hours = rng.uniform(0, 40)
        for day in range(days):
            vibration = float(rng.normal(2.8 + 0.15 * machine_index, 0.45))
            temperature = float(rng.normal(62 + machine_index, 3.5))
            pressure = float(rng.normal(5.5, 0.35))
            runtime = float(rng.uniform(6, 10))
            probability = float(_failure_probability(np.array([vibration]), np.array([temperature]), np.array([hours]))[0])
            failure = int(rng.random() < probability)
            rows.append(
                {
                    "date": START + pd.Timedelta(days=day),
                    "machine_id": machine,
                    "vibration_mm_s": round(vibration, 3),
                    "temperature_c": round(temperature, 2),
                    "pressure_bar": round(pressure, 3),
                    "hours_since_maintenance": round(float(hours), 2),
                    "runtime_hours": round(runtime, 2),
                    "failure": failure,
                }
            )
            hours = 0.0 if failure else hours + runtime
    return pd.DataFrame(rows)


def write_raw_data(root: Path, seed: int = SEED) -> pd.DataFrame:
    raw = root / "data" / "raw"
    raw.mkdir(parents=True, exist_ok=True)
    frame = machine_days(seed=seed)
    frame.to_csv(raw / "machine_days.csv", index=False)
    return frame
