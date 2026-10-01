"""Charts for the capstone story."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from kpi import add_measures

BLUE = "#1f4e79"
ORANGE = "#c45911"


def _style(ax, title: str, ylabel: str) -> None:
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def save_attainment(shift_table: pd.DataFrame, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(shift_table["shift"], shift_table["attainment"], color=[BLUE, ORANGE])
    ax.set_ylim(0, 1)
    _style(ax, "Production attainment by shift", "Actual / planned")
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)


def save_scrap_by_machine(production: pd.DataFrame, path: Path) -> None:
    frame = add_measures(production)
    grouped = frame.groupby("machine_id", as_index=False).agg(scrap_qty=("scrap_qty", "sum"), actual_qty=("actual_qty", "sum"))
    grouped["scrap_rate"] = grouped["scrap_qty"] / grouped["actual_qty"]
    grouped = grouped.sort_values("scrap_rate", ascending=False)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(grouped["machine_id"], grouped["scrap_rate"], color=BLUE)
    _style(ax, "Scrap rate by machine", "Scrap / actual")
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)


def save_downtime(reasons: pd.DataFrame, path: Path) -> None:
    ordered = reasons.sort_values("downtime_min", ascending=True)
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.barh(ordered["reason"], ordered["downtime_min"], color=ORANGE)
    _style(ax, "Downtime minutes by reason", "Minutes")
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)
