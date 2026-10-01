"""Write the capstone summary from SQL, pandas and the statistical test."""

import json
from pathlib import Path

import pandas as pd


def write_summary(answers: dict[str, pd.DataFrame], shift_test: dict, scrap_interval: dict, path: Path) -> dict:
    gap = answers["orders_against_good_units"].sort_values("gap")
    short = gap.iloc[0]
    reasons = answers["downtime_by_reason"]
    top_reason = reasons.iloc[0]
    attainment = answers["attainment_by_shift"].set_index("shift")
    p_value = float(shift_test["p_value"])
    p_text = "< 0.0001" if p_value < 0.0001 else f"{p_value:.4f}"
    metrics = {
        "short_product": str(short["product"]),
        "short_gap": int(short["gap"]),
        "top_downtime_reason": str(top_reason["reason"]),
        "top_downtime_min": int(top_reason["downtime_min"]),
        "morning_attainment": round(float(attainment.loc["Morning", "attainment"]), 4),
        "night_attainment": round(float(attainment.loc["Night", "attainment"]), 4),
        "morning_mean_good": round(shift_test["morning_mean_good"], 1),
        "night_mean_good": round(shift_test["night_mean_good"], 1),
        "p_value": float(shift_test["p_value"]),
        "scrap_rate": round(scrap_interval["mean_daily_scrap_rate"], 4),
        "scrap_low": round(scrap_interval["low"], 4),
        "scrap_high": round(scrap_interval["high"], 4),
    }
    lines = [
        "# Operations capstone summary",
        "",
        "One synthetic quarter. SQL, pandas and the statistical test use the same tables.",
        "",
        (
            f"{metrics['short_product']} finished {abs(metrics['short_gap'])} good units behind orders."
            if metrics["short_gap"] < 0
            else f"{metrics['short_product']} finished {metrics['short_gap']} good units ahead of orders."
        ),
        f"Largest downtime reason: {metrics['top_downtime_reason']} ({metrics['top_downtime_min']} minutes).",
        (
            f"Attainment is {metrics['morning_attainment']:.1%} in the morning and "
            f"{metrics['night_attainment']:.1%} at night."
        ),
        (
            f"Mean daily good units are {metrics['morning_mean_good']} in the morning and "
            f"{metrics['night_mean_good']} at night. The Welch t-test p-value is {p_text}."
        ),
        (
            f"Mean daily scrap rate is {metrics['scrap_rate']:.2%}, with a 95% interval from "
            f"{metrics['scrap_low']:.2%} to {metrics['scrap_high']:.2%}. "
            "The interval is narrow because the daily scrap rate barely moves in this sample."
        ),
        "",
        "## Orders against good units",
        "",
        _markdown_table(gap),
        "",
        "## How to explain the limitation",
        "",
        "The night shift was given more downtime in the simulator, so a small p-value shows that the sample preserves that pattern. It does not prove a cause in a real plant. Each row also keeps one downtime reason, so a shift with two problems is recorded as the larger bucket only.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")
    return metrics


def write_metrics(metrics: dict, path: Path) -> None:
    path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")


def _markdown_table(frame: pd.DataFrame) -> str:
    header = "| " + " | ".join(frame.columns) + " |"
    rule = "| " + " | ".join("---" for _ in frame.columns) + " |"
    body = [
        "| " + " | ".join(str(value) for value in row) + " |"
        for row in frame.itertuples(index=False, name=None)
    ]
    return "\n".join([header, rule, *body])
