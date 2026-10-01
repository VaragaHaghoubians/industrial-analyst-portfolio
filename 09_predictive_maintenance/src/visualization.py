"""Charts for the rare-failure comparison."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

BLUE = "#1f4e79"
ORANGE = "#c45911"


def save_class_balance(failure_rate: float, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(["No failure", "Failure"], [1 - failure_rate, failure_rate], color=[BLUE, ORANGE])
    ax.set_ylim(0, 1)
    ax.set_ylabel("Share of days")
    ax.set_title("Failures are the rare class")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)


def save_recall_comparison(baseline_recall: float, model_recall: float, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(["Always no failure", "Balanced logistic regression"], [baseline_recall, model_recall], color=[BLUE, ORANGE])
    ax.set_ylim(0, 1)
    ax.set_ylabel("Recall on the test days")
    ax.set_title("Catching failures, not just looking accurate")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)


def save_confusion_matrix(matrix: list, path: Path) -> None:
    values = np.array(matrix)
    fig, ax = plt.subplots(figsize=(5, 4))
    image = ax.imshow(values, cmap="Blues")
    ax.set_xticks([0, 1], ["Predicted no", "Predicted failure"])
    ax.set_yticks([0, 1], ["Actual no", "Actual failure"])
    ax.set_title("Test confusion matrix")
    for row in range(2):
        for col in range(2):
            ax.text(col, row, str(values[row, col]), ha="center", va="center", color="black")
    fig.colorbar(image, ax=ax, fraction=0.046)
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)
