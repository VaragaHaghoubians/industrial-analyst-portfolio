"""Compare a majority-class baseline with a balanced logistic regression.

Accuracy is a weak score when failures are rare. Predicting "no failure"
every day can look accurate and still miss every failure. Recall asks a
better question: of the failures that happened, how many did the model catch?
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from cleaning import FEATURES


def _scores(y_true, y_pred) -> dict:
    matrix = confusion_matrix(y_true, y_pred, labels=[0, 1])
    return {
        "accuracy": float((y_pred == y_true).mean()),
        "precision": float(precision_score(y_true, y_pred, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, zero_division=0)),
        "confusion_matrix": matrix.tolist(),
    }


def train_and_compare(frame: pd.DataFrame, seed: int = 42, test_size: float = 0.30) -> dict:
    work = frame.sample(frac=1.0, random_state=seed).reset_index(drop=True)
    x_train, x_test, y_train, y_test = train_test_split(
        work[FEATURES],
        work["failure"],
        test_size=test_size,
        random_state=seed,
        stratify=work["failure"],
    )
    baseline_pred = np.zeros(len(y_test), dtype=int)
    pipeline = Pipeline(
        [
            ("scale", StandardScaler()),
            (
                "model",
                LogisticRegression(class_weight="balanced", max_iter=1000, random_state=seed),
            ),
        ]
    )
    pipeline.fit(x_train, y_train)
    model_pred = pipeline.predict(x_test)
    coefficients = pipeline.named_steps["model"].coef_[0]
    importance = (
        pd.DataFrame({"feature": FEATURES, "coefficient": coefficients})
        .assign(abs_coefficient=lambda frame_: frame_["coefficient"].abs())
        .sort_values("abs_coefficient", ascending=False)
    )
    return {
        "rows": int(len(frame)),
        "failure_rate": float(frame["failure"].mean()),
        "train_rows": int(len(x_train)),
        "test_rows": int(len(y_test)),
        "test_failures": int(y_test.sum()),
        "baseline": _scores(y_test.to_numpy(), baseline_pred),
        "model": _scores(y_test.to_numpy(), model_pred),
        "coefficients": importance,
        "pipeline": pipeline,
    }
