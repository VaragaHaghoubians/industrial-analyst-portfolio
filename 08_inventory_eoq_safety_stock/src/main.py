"""Run the inventory project from raw demand to the summary."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cleaning import clean_inputs
from generate_data import write_raw_data
from inventory import build_policy, service_level_curve
from reporting import write_metrics, write_summary
from visualization import save_cost_curve, save_safety_stock, save_stock_versus_reorder


def main() -> None:
    weekly, master = write_raw_data(ROOT)
    weekly, master = clean_inputs(weekly, master)
    policy = build_policy(weekly, master)
    top = policy.sort_values("safety_stock", ascending=False).iloc[0]
    curve = service_level_curve(float(top["weekly_std"]), float(top["lead_time_weeks"]))

    processed = ROOT / "data" / "processed"
    figures = ROOT / "reports" / "figures"
    processed.mkdir(parents=True, exist_ok=True)
    figures.mkdir(parents=True, exist_ok=True)
    policy.to_csv(processed / "inventory_policy.csv", index=False)
    curve.to_csv(processed / "service_level_curve.csv", index=False)

    save_cost_curve(policy, figures / "eoq_cost_curve.png")
    save_safety_stock(policy, figures / "safety_stock_by_sku.png")
    save_stock_versus_reorder(policy, figures / "on_hand_vs_reorder_point.png")
    metrics = write_summary(policy, curve, ROOT / "reports" / "inventory_summary.md")
    write_metrics(metrics, ROOT / "reports" / "metrics.json")

    print(policy[["sku", "order_qty", "safety_stock", "reorder_point", "on_hand", "action"]].round(1).to_string(index=False))
    print()
    print(f"Reorder now: {', '.join(metrics['reorder_now'])}")
    print(f"High stock: {', '.join(metrics['high_stock'])}")


if __name__ == "__main__":
    main()
