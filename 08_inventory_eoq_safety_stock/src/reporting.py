"""Write the inventory summary from the calculated policy table."""

import json
from pathlib import Path

import pandas as pd


def write_summary(policy: pd.DataFrame, curve: pd.DataFrame, path: Path) -> dict:
    reorder = policy.loc[policy["action"] == "Reorder now", "sku"].tolist()
    high = policy.loc[policy["action"] == "Stock is high, review", "sku"].tolist()
    top_ss = policy.sort_values("safety_stock", ascending=False).iloc[0]
    top_cost = policy.sort_values("total_relevant_cost", ascending=False).iloc[0]
    by_level = dict(zip(curve["service_level"], curve["safety_stock"]))
    per_point_low = (by_level[0.95] - by_level[0.90]) / 5
    per_point_high = by_level[0.99] - by_level[0.98]
    metrics = {
        "sku_count": int(len(policy)),
        "reorder_now": reorder,
        "high_stock": high,
        "highest_safety_stock_sku": str(top_ss["sku"]),
        "highest_safety_stock_units": round(float(top_ss["safety_stock"]), 1),
        "highest_relevant_cost_sku": str(top_cost["sku"]),
        "highest_relevant_cost_euro": round(float(top_cost["total_relevant_cost"]), 2),
        "total_relevant_cost_euro": round(float(policy["total_relevant_cost"].sum()), 2),
    }
    lines = [
        "# Inventory policy summary",
        "",
        "Synthetic demand for one year. These figures are calculated from the sample, not typed in as a result.",
        "",
        f"SKUs in the policy: {metrics['sku_count']}.",
        f"Reorder now: {', '.join(reorder) if reorder else 'none'}.",
        f"Stock is high and should be reviewed: {', '.join(high) if high else 'none'}.",
        (
            f"Highest safety stock is {metrics['highest_safety_stock_sku']} "
            f"at {metrics['highest_safety_stock_units']} units."
        ),
        (
            f"Highest relevant order-and-hold cost is {metrics['highest_relevant_cost_sku']} "
            f"at {metrics['highest_relevant_cost_euro']:.2f} euro per year."
        ),
        f"Total relevant cost across SKUs: {metrics['total_relevant_cost_euro']:.2f} euro per year.",
        "",
        "Relevant cost here means ordering cost plus holding cost of the cycle stock. It does not include the purchase price of the parts.",
        "",
        "## Policy table",
        "",
        _markdown_table(
            policy[
                [
                    "sku",
                    "order_qty",
                    "safety_stock",
                    "reorder_point",
                    "on_hand",
                    "action",
                ]
            ].round(1)
        ),
        "",
        "## Safety stock if the service level changes",
        "",
        (
            "The curve below uses the weekly variation and lead time of "
            f"{metrics['highest_safety_stock_sku']}. "
            f"Each percentage point from 90% to 95% adds about {per_point_low:.1f} units. "
            f"The single point from 98% to 99% adds about {per_point_high:.1f} units."
        ),
        "",
        _markdown_table(_format_curve(curve)),
        "",
        "## How to explain the limitation",
        "",
        "Lead time does not vary in this model. A late supplier would need a larger buffer than the table shows. Demand is also synthetic, so the actions are a method demo, not a purchasing decision.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")
    return metrics


def write_metrics(metrics: dict, path: Path) -> None:
    path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")


def _format_curve(curve: pd.DataFrame) -> pd.DataFrame:
    display = curve.copy()
    display["service_level"] = display["service_level"].map(lambda value: f"{value:.0%}")
    display["safety_stock"] = display["safety_stock"].round(1)
    return display


def _markdown_table(frame: pd.DataFrame) -> str:
    display = frame.copy()
    header = "| " + " | ".join(display.columns) + " |"
    rule = "| " + " | ".join("---" for _ in display.columns) + " |"
    body = [
        "| " + " | ".join(str(value) for value in row) + " |"
        for row in display.itertuples(index=False, name=None)
    ]
    return "\n".join([header, rule, *body])
