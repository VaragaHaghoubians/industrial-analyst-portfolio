"""A shift comparison and a confidence interval for the daily scrap rate."""

import pandas as pd
from scipy import stats

from kpi import add_measures


def compare_shifts(production: pd.DataFrame) -> dict:
    daily = (
        add_measures(production)
        .groupby(["date", "shift"], as_index=False)["good_qty"]
        .sum()
    )
    morning = daily.loc[daily["shift"] == "Morning", "good_qty"]
    night = daily.loc[daily["shift"] == "Night", "good_qty"]
    test = stats.ttest_ind(morning, night, equal_var=False)
    return {
        "morning_mean_good": float(morning.mean()),
        "night_mean_good": float(night.mean()),
        "t_statistic": float(test.statistic),
        "p_value": float(test.pvalue),
        "morning_days": int(morning.shape[0]),
        "night_days": int(night.shape[0]),
    }


def scrap_rate_interval(production: pd.DataFrame, confidence: float = 0.95) -> dict:
    frame = add_measures(production)
    daily = frame.groupby("date", as_index=False).agg(scrap_qty=("scrap_qty", "sum"), actual_qty=("actual_qty", "sum"))
    daily["scrap_rate"] = daily["scrap_qty"] / daily["actual_qty"]
    mean = float(daily["scrap_rate"].mean())
    interval = stats.t.interval(
        confidence,
        len(daily) - 1,
        loc=mean,
        scale=stats.sem(daily["scrap_rate"]),
    )
    return {
        "days": int(len(daily)),
        "mean_daily_scrap_rate": mean,
        "low": float(interval[0]),
        "high": float(interval[1]),
        "confidence": confidence,
    }
