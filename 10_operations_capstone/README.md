# Project 10, one operations story

One synthetic quarter ties the earlier skills together. SQL compares orders with good units. Pandas calculates attainment and scrap. A Welch t-test compares morning and night. A CSV is ready for a Power BI page.

The folder layout matches the steel manufacturing project. The night shift was given more downtime in the simulator, so the gap is a pattern in the sample, not proof of a cause in a plant.

## Result on the sample data

Bracket finished 2,342 good units behind orders. Housing finished 448 good units ahead.

Attainment is 96.3% in the morning and 89.4% at night. Mean daily good units are 281.8 in the morning and 208.5 at night. The Welch p-value is below 0.0001.

Breakdown is the largest downtime bucket, 10,220 minutes. The mean daily scrap rate is 2.61%, and the 95% interval is only 2.60% to 2.63% because the daily rate barely moves.

Details are in [reports/capstone_summary.md](reports/capstone_summary.md).

## How to run it

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe .\src\main.py
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Open [START_HERE.md](START_HERE.md), then [dashboard/POWER_BI_STEPS.md](dashboard/POWER_BI_STEPS.md) if you build the page. The portfolio MIT license in the repository root covers this folder.

## What I learned

The same total should come out of SQL and pandas. If those two disagree, one of them is wrong.

Attainment is actual quantity divided by planned quantity. Good quantity is actual minus scrap.

A very small p-value means the morning and night samples are easy to tell apart. Here that is expected, because the generator gave the night shift more downtime.

A narrow confidence interval means the average is estimated tightly. It does not mean scrap is unimportant.

## Repository structure

```text
10_operations_capstone/
├── README.md, START_HERE.md, requirements.txt
├── data/raw/                 # production and orders
├── data/processed/           # SQL answers and the Power BI extract
├── notebooks/
├── src/                      # SQL, pandas, statistics, charts
├── reports/
├── docs/
├── dashboard/                # Power BI steps
└── tests/                    # SQL matches pandas
```
