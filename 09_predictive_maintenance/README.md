# Project 9, predictive maintenance

Four machines, 180 synthetic days, and a failure on about 7.8% of those days. The point of the project is the rare class. A model that always says "no failure" is 92.1% accurate on the test days and still catches none of the failures.

A logistic regression with balanced class weights catches 64.7% of the test failures. Its precision is 25.6%, so most alarms are false. That tradeoff is the result, not a tuning accident. The numbers are in [reports/maintenance_summary.md](reports/maintenance_summary.md).

The folder layout matches the steel manufacturing project. The readings are synthetic. This is not a claim about a real machine.

## How to run it

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe .\src\main.py
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Open [START_HERE.md](START_HERE.md) first. The portfolio MIT license in the repository root covers this folder.

## What I learned

Accuracy hides a rare event. Recall asks how many real failures were caught. Precision asks how many alarms were real.

`class_weight="balanced"` tells logistic regression that a missed failure matters more than a quiet day. Accuracy can fall while recall rises. That is the intended tradeoff here.

The largest coefficient, after scaling, is hours since maintenance. Pressure also gets a coefficient even though the simulator does not use pressure to create failures. A coefficient is not a cause.

## Repository structure

```text
09_predictive_maintenance/
├── README.md, START_HERE.md, requirements.txt
├── data/raw/machine_days.csv
├── data/processed/           # clean rows and coefficients
├── notebooks/
├── src/
├── reports/                  # class balance, recall, confusion matrix
├── docs/
├── dashboard/README.md
└── tests/
```
