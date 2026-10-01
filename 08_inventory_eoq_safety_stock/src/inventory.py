"""EOQ, safety stock and reorder point.

EOQ balances order cost against holding cost. Safety stock covers demand
variation during the lead time. The reorder point is expected demand during
the lead time plus that safety stock.

Lead time is treated as constant. Weekly demands are treated as independent.
Those two choices keep the formulas short enough to explain in an interview.
"""

import math

import pandas as pd
from scipy.stats import norm


def economic_order_quantity(annual_demand: float, order_cost: float, holding_cost_per_unit: float) -> float:
    if annual_demand <= 0 or order_cost <= 0 or holding_cost_per_unit <= 0:
        raise ValueError("EOQ needs positive demand, order cost and holding cost.")
    return math.sqrt(2 * annual_demand * order_cost / holding_cost_per_unit)


def order_policy_cost(annual_demand: float, order_cost: float, holding_cost_per_unit: float, quantity: float) -> dict:
    if quantity <= 0:
        raise ValueError("Order quantity must be positive.")
    ordering = annual_demand / quantity * order_cost
    holding = quantity / 2 * holding_cost_per_unit
    return {
        "ordering_cost": ordering,
        "holding_cost": holding,
        "total_relevant_cost": ordering + holding,
    }


def z_score(service_level: float) -> float:
    if not 0.5 < service_level < 1:
        raise ValueError("Service level must be between 0.5 and 1.")
    return float(norm.ppf(service_level))


def safety_stock(weekly_std: float, lead_time_weeks: float, service_level: float) -> float:
    if weekly_std < 0 or lead_time_weeks <= 0:
        raise ValueError("Standard deviation cannot be negative and lead time must be positive.")
    return z_score(service_level) * weekly_std * math.sqrt(lead_time_weeks)


def build_policy(weekly: pd.DataFrame, master: pd.DataFrame) -> pd.DataFrame:
    master_by_sku = master.set_index("sku")
    rows = []
    for sku, group in weekly.groupby("sku", sort=False):
        info = master_by_sku.loc[sku]
        annual_demand = float(group["demand_units"].sum())
        weekly_mean = float(group["demand_units"].mean())
        weekly_std = float(group["demand_units"].std(ddof=1))
        holding_cost = float(info["unit_cost"]) * float(info["holding_rate"])
        eoq = economic_order_quantity(annual_demand, float(info["order_cost"]), holding_cost)
        order_qty = max(1, int(round(eoq)))
        costs = order_policy_cost(annual_demand, float(info["order_cost"]), holding_cost, order_qty)
        ss = safety_stock(weekly_std, float(info["lead_time_weeks"]), float(info["service_level"]))
        lead_time_demand = weekly_mean * float(info["lead_time_weeks"])
        reorder_point = lead_time_demand + ss
        on_hand = int(info["on_hand"])
        if on_hand <= reorder_point:
            action = "Reorder now"
        elif on_hand > reorder_point + order_qty:
            action = "Stock is high, review"
        else:
            action = "Inside the band"
        rows.append(
            {
                "sku": sku,
                "category": info["category"],
                "annual_demand": annual_demand,
                "weekly_mean": weekly_mean,
                "weekly_std": weekly_std,
                "holding_cost_per_unit": holding_cost,
                "order_cost": float(info["order_cost"]),
                "eoq": eoq,
                "order_qty": order_qty,
                "ordering_cost": costs["ordering_cost"],
                "holding_cost": costs["holding_cost"],
                "total_relevant_cost": costs["total_relevant_cost"],
                "service_level": float(info["service_level"]),
                "z_score": z_score(float(info["service_level"])),
                "lead_time_weeks": int(info["lead_time_weeks"]),
                "lead_time_demand": lead_time_demand,
                "safety_stock": ss,
                "reorder_point": reorder_point,
                "on_hand": on_hand,
                "weeks_of_cover": on_hand / weekly_mean if weekly_mean else float("nan"),
                "action": action,
            }
        )
    return pd.DataFrame(rows)


def service_level_curve(weekly_std: float, lead_time_weeks: float, levels: list[float] | None = None) -> pd.DataFrame:
    if levels is None:
        levels = [0.90, 0.95, 0.97, 0.98, 0.99]
    return pd.DataFrame(
        {
            "service_level": levels,
            "safety_stock": [safety_stock(weekly_std, lead_time_weeks, level) for level in levels],
        }
    )
