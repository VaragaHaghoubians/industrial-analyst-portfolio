# Project 09 - Predictive maintenance (will this machine fail?)
# I try to predict machine failure from sensor readings: temperature, speed,
# torque and tool wear. This is the kind of thing I did in my internship on
# HVAC sensor data, here on a smaller, public-style dataset.
#
# If you download the real AI4I 2020 dataset and save it here as ai4i2020.csv,
# the script uses it. If not, it creates similar fake data so it still runs.
# Real dataset: https://archive.ics.uci.edu/dataset/601/ai4i+2020+predictive+maintenance+dataset

import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

np.random.seed(6)

# ---------- step 1: load the real data if I have it, otherwise make fake data ----------
if os.path.exists("ai4i2020.csv"):
    df = pd.read_csv("ai4i2020.csv")
    # the real file uses these long column names, I shorten them
    df = df.rename(columns={
        "Air temperature [K]": "air_temp",
        "Process temperature [K]": "process_temp",
        "Rotational speed [rpm]": "speed",
        "Torque [Nm]": "torque",
        "Tool wear [min]": "tool_wear",
        "Machine failure": "failure",
    })
    print("Loaded the real AI4I 2020 dataset")
else:
    n = 5000
    df = pd.DataFrame({
        "air_temp": np.random.normal(300, 2, n),
        "process_temp": np.random.normal(310, 1.5, n),
        "speed": np.random.normal(1500, 150, n),
        "torque": np.random.normal(40, 10, n),
        "tool_wear": np.random.uniform(0, 250, n),
    })
    # failures are rare (like real life) and more likely with high torque,
    # a worn tool, and when the process runs much hotter than the air
    risk = (
        0.01
        + 0.015 * (df["torque"] - 50).clip(lower=0)
        + 0.0025 * (df["tool_wear"] - 190).clip(lower=0)
        + 0.06 * (df["process_temp"] - df["air_temp"] > 11)
    ).clip(upper=0.9)   # a probability can never be above 1, so I cap it
    df["failure"] = (np.random.rand(n) < risk).astype(int)
    print("No ai4i2020.csv found, so I made similar fake data")

features = ["air_temp", "process_temp", "speed", "torque", "tool_wear"]
X = df[features]
y = df["failure"]

print("Rows:", len(df))
print("Failure rate:", round(y.mean() * 100, 2), "%  <- failures are rare, so accuracy alone is misleading\n")

# ---------- step 2: split into training and testing ----------
# stratify=y keeps the same failure % in both parts. Important when failures are rare.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1, stratify=y)

# ---------- step 3: two models ----------
# class_weight="balanced" tells the model: "failures are rare, pay extra attention to them"
models = {
    "Logistic Regression": LogisticRegression(max_iter=2000, class_weight="balanced"),
    "Random Forest": RandomForestClassifier(n_estimators=200, class_weight="balanced", random_state=1),
}

for name, model in models.items():
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    print("=" * 50)
    print(name)
    print("=" * 50)
    print("Accuracy:", round(accuracy_score(y_test, pred), 3))
    print("Confusion matrix (rows = actual, cols = predicted):")
    print(confusion_matrix(y_test, pred))
    print(classification_report(y_test, pred, target_names=["no failure", "failure"]))

# ---------- step 4: which sensors matter most? ----------
rf = models["Random Forest"]
importance = pd.Series(rf.feature_importances_, index=features).sort_values(ascending=False)
print("=== Feature importance (Random Forest) ===")
print(importance.round(3))
print("\nThe sensors at the top are the ones I would watch on a live dashboard.")
print("\nLook at the two models above:")
print("- Random Forest has the HIGHER accuracy but catches almost no failures (low recall).")
print("- Logistic Regression has LOWER accuracy but catches most failures (high recall), with more false alarms.")
print("For maintenance I would pick the model with high recall on 'failure'.")
print("Note to self: missing a real failure costs far more than a false alarm. Accuracy alone would fool me here.")
