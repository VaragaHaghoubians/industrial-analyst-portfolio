# Industrial / Operations Data Analyst, my portfolio

![Python](https://img.shields.io/badge/python-3.10%2B-blue) ![License](https://img.shields.io/badge/license-MIT-green)

Hi, I'm Varaga. I have a BSc in Industrial Engineering and I am finishing an MSc in Data Science in Turin. This repo is my collection of small, beginner friendly projects that show the skills an Industrial / Operations Data Analyst uses every day, SQL, Python with pandas, Power BI, statistics, forecasting, optimization, inventory and predictive maintenance.

I'm doing these projects and pushing them here as I finish them. Each one has its own README with what it does, how to run it, and what I learned.

Every project makes its own sample data, so you can run it right away, no downloads needed.

## The 10 projects

| # | Project | Tier | What it shows | Main tools |
|---|---|---|---|---|
| 1 | [SQL business questions](01_sql_business_questions/) | Master | JOIN, GROUP BY, window functions, CTE | sqlite3 |
| 2 | [Clean messy data](02_clean_messy_data/) | Master | missing values, duplicates, wrong types, sensor errors | pandas |
| 3 | [EDA on operations data](03_eda_operations/) | Master | groupby, pivot tables, charts, 3 findings | pandas, matplotlib |
| 4 | [KPI dashboard in Power BI](04_kpi_dashboard_powerbi/) | Master | KPI dataset plus a Power BI dashboard with DAX measures | pandas, Power BI |
| 5 | [Statistics report](05_statistics_report/) | Master | descriptive stats, t-test, confidence interval, correlation | scipy, pandas |
| 6 | [Demand forecasting](06_demand_forecasting/) | Edge | naive baselines against Holt-Winters, MAPE | statsmodels |
| 7 | Production mix optimizer | Edge | linear programming, finding the bottleneck | PuLP |
| 8 | Inventory, EOQ and safety stock | Edge | EOQ, reorder point, safety stock, service level | math, scipy |
| 9 | Predictive maintenance | Edge | classifying machine failure, handling a rare class | scikit-learn |
| 10 | Capstone, one operations story | Both | SQL, then pandas, then statistics, then Power BI, all together | everything above |

Master means the core analyst skills. Edge means my industrial engineering side.

## How to run

Install Python 3.10 or newer, then install the libraries:

```
pip install -r requirements.txt
```

Go into a project folder and run the script, for example:

```
cd 01_sql_business_questions
python sql_questions.py
```

Each script prints its results and saves any charts or csv files in its own folder.

## A bit about me

BSc Industrial Engineering, and an MSc in Stochastics and Data Science at the University of Turin.

Internship doing anomaly detection on real industrial HVAC and IoT sensor data, which is predictive maintenance.

Before that, industrial data monitoring and KPI dashboards for production managers.
