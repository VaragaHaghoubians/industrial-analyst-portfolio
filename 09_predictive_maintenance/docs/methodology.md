# Methodology

The published run uses seed 42.

Cleaning checks one row per machine per day, a 0/1 label, and no missing or negative readings.

The comparison uses one stratified holdout: 70% train, 30% test, random state 42. Stratified means the test set keeps the same failure share as the full sample. It is not a test of a future month. A time-based split would be the next check on a real historian.

The baseline predicts 0 for every test row.

The model is a pipeline. `StandardScaler` puts each input on a similar scale. `LogisticRegression(class_weight="balanced")` then fits a line in that scaled space. The decision threshold stays at 0.5.

Reported scores are accuracy, precision and recall on the test rows only. The confusion matrix counts true quiet days, false alarms, missed failures and caught failures.
