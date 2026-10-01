"""Train the rare-failure comparison and save the charts."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cleaning import clean_readings
from generate_data import write_raw_data
from model import train_and_compare
from reporting import write_metrics, write_summary
from visualization import save_class_balance, save_confusion_matrix, save_recall_comparison


def main() -> None:
    frame = clean_readings(write_raw_data(ROOT))
    result = train_and_compare(frame)
    processed = ROOT / "data" / "processed"
    figures = ROOT / "reports" / "figures"
    processed.mkdir(parents=True, exist_ok=True)
    figures.mkdir(parents=True, exist_ok=True)
    frame.to_csv(processed / "machine_days_clean.csv", index=False)
    result["coefficients"].to_csv(processed / "coefficients.csv", index=False)

    save_class_balance(result["failure_rate"], figures / "class_balance.png")
    save_recall_comparison(result["baseline"]["recall"], result["model"]["recall"], figures / "recall_comparison.png")
    save_confusion_matrix(result["model"]["confusion_matrix"], figures / "confusion_matrix.png")
    metrics = write_summary(result, ROOT / "reports" / "maintenance_summary.md")
    write_metrics(metrics, ROOT / "reports" / "metrics.json")
    print(
        f"Failure rate {metrics['failure_rate']:.1%}. "
        f"Baseline recall {metrics['baseline_recall']:.1%}. "
        f"Model recall {metrics['model_recall']:.1%}, precision {metrics['model_precision']:.1%}."
    )


if __name__ == "__main__":
    main()
