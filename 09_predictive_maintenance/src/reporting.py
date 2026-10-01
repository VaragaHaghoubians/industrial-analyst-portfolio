"""Write the maintenance-model summary from the calculated scores."""

import json
from pathlib import Path

import pandas as pd


def write_summary(result: dict, path: Path) -> dict:
    baseline = result["baseline"]
    model = result["model"]
    top = result["coefficients"].iloc[0]
    metrics = {
        "rows": result["rows"],
        "failure_rate": round(result["failure_rate"], 4),
        "test_failures": result["test_failures"],
        "baseline_accuracy": round(baseline["accuracy"], 4),
        "baseline_recall": round(baseline["recall"], 4),
        "model_accuracy": round(model["accuracy"], 4),
        "model_precision": round(model["precision"], 4),
        "model_recall": round(model["recall"], 4),
        "strongest_feature": str(top["feature"]),
        "strongest_coefficient": round(float(top["coefficient"]), 3),
    }
    lines = [
        "# Predictive maintenance summary",
        "",
        "Synthetic daily readings. The scores below come from one stratified holdout, not from a typed-in target.",
        "",
        f"Rows: {metrics['rows']}. Failure rate: {metrics['failure_rate']:.1%}.",
        f"Test failures: {metrics['test_failures']}.",
        (
            f"Always predicting no failure has accuracy {metrics['baseline_accuracy']:.1%} "
            f"and recall {metrics['baseline_recall']:.1%}."
        ),
        (
            f"Balanced logistic regression has accuracy {metrics['model_accuracy']:.1%}, "
            f"precision {metrics['model_precision']:.1%} and recall {metrics['model_recall']:.1%}."
        ),
        (
            f"After scaling, the largest coefficient is {metrics['strongest_feature']} "
            f"({metrics['strongest_coefficient']})."
        ),
        "",
        "A positive coefficient means a higher value raises the chance of a predicted failure. Precision says how many predicted failures were real. Recall says how many real failures were caught. A coefficient is not a cause. Pressure was not part of the failure rule, so its coefficient is only a fit to this sample.",
        "",
        "## Coefficients",
        "",
        _markdown_table(result["coefficients"].drop(columns=["abs_coefficient"]).round(3)),
        "",
        "## How to explain the limitation",
        "",
        "The split is random within the sample, so it is not a true future-week test. The failure rule was written into the simulator, which is why a simple model can find it. A real historian has sensor drift, maintenance notes and failures that do not follow a clean formula.",
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
