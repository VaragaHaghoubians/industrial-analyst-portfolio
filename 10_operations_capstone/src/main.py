"""Run SQL, pandas, the statistical test and the Power BI extract."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cleaning import clean_tables
from generate_data import write_raw_data
from kpi import dashboard_table, shift_summary
from reporting import write_metrics, write_summary
from sql_questions import run_questions
from shift_stats import compare_shifts, scrap_rate_interval
from visualization import save_attainment, save_downtime, save_scrap_by_machine


def main() -> None:
    production, orders = clean_tables(*write_raw_data(ROOT))
    answers = run_questions(production, orders)
    shifts = shift_summary(production)
    shift_test = compare_shifts(production)
    scrap_interval = scrap_rate_interval(production)

    processed = ROOT / "data" / "processed"
    figures = ROOT / "reports" / "figures"
    processed.mkdir(parents=True, exist_ok=True)
    figures.mkdir(parents=True, exist_ok=True)
    for name, frame in answers.items():
        frame.to_csv(processed / f"{name}.csv", index=False)
    dashboard_table(production).to_csv(processed / "kpi_data.csv", index=False)
    shifts.to_csv(processed / "shift_summary.csv", index=False)

    save_attainment(shifts, figures / "attainment_by_shift.png")
    save_scrap_by_machine(production, figures / "scrap_by_machine.png")
    save_downtime(answers["downtime_by_reason"], figures / "downtime_by_reason.png")
    metrics = write_summary(answers, shift_test, scrap_interval, ROOT / "reports" / "capstone_summary.md")
    write_metrics(metrics, ROOT / "reports" / "metrics.json")
    print(answers["orders_against_good_units"].to_string(index=False))
    print(
        f"Morning attainment {metrics['morning_attainment']:.1%}, "
        f"night {metrics['night_attainment']:.1%}, p-value {metrics['p_value']}."
    )


if __name__ == "__main__":
    main()
