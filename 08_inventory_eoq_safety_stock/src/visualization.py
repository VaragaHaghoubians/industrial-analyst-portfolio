"""Charts for the inventory policy."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from inventory import order_policy_cost

BLUE = "#1f4e79"
ORANGE = "#c45911"


def _style(ax, title: str, ylabel: str) -> None:
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def save_cost_curve(policy: pd.DataFrame, path: Path) -> str:
    row = policy.sort_values("annual_demand", ascending=False).iloc[0]
    quantities = np.linspace(max(1, row["eoq"] * 0.25), row["eoq"] * 2.2, 80)
    ordering, holding = [], []
    for quantity in quantities:
        cost = order_policy_cost(
            row["annual_demand"],
            row["order_cost"],
            row["holding_cost_per_unit"],
            float(quantity),
        )
        ordering.append(cost["ordering_cost"])
        holding.append(cost["holding_cost"])
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(quantities, ordering, color=BLUE, label="Ordering cost")
    ax.plot(quantities, holding, color=ORANGE, label="Holding cost")
    ax.plot(quantities, np.array(ordering) + np.array(holding), color="#548235", label="Total relevant cost")
    ax.axvline(row["eoq"], color="#7f7f7f", linestyle="--", label=f"EOQ {row['eoq']:.0f}")
    _style(ax, f"{row['sku']}: cost against order quantity", "Euro per year")
    ax.set_xlabel("Order quantity (units)")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)
    return str(row["sku"])


def save_safety_stock(policy: pd.DataFrame, path: Path) -> None:
    ordered = policy.sort_values("safety_stock", ascending=True)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.barh(ordered["sku"], ordered["safety_stock"], color=BLUE)
    _style(ax, "Safety stock by SKU", "Units")
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)


def save_stock_versus_reorder(policy: pd.DataFrame, path: Path) -> None:
    ordered = policy.sort_values("reorder_point", ascending=False)
    y = np.arange(len(ordered))
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.barh(y - 0.18, ordered["on_hand"], height=0.36, color=BLUE, label="On hand")
    ax.barh(y + 0.18, ordered["reorder_point"], height=0.36, color=ORANGE, label="Reorder point")
    ax.set_yticks(y, ordered["sku"])
    _style(ax, "On-hand stock against the reorder point", "Units")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)
