# Industrial / Operations Data Analyst: My Portfolio

![Python](https://img.shields.io/badge/python-3.10%2B-blue) ![License](https://img.shields.io/badge/license-MIT-green)

Sample-data exercises for an industrial / operations analyst application: SQL, pandas cleaning, EDA, a small statistics report, forecasting, a production-mix linear program, inventory, and a failure classifier.

Project 4 prepares a KPI extract and lists Power BI steps. It does not include a `.pbix` or a dashboard screenshot. Project 10 is an unfilled template. Each exercise generates its own sample data.

## The 10 projects

| # | Project | Tier | What it shows | Main tools |
|---|---|---|---|---|
| 1 | [SQL business questions](01_sql_business_questions/) | Master | JOIN, GROUP BY, window functions, CTE | sqlite3 |
| 2 | [Clean messy data](02_clean_messy_data/) | Master | missing values, duplicates, wrong types, sensor errors | pandas |
| 3 | [EDA on operations data](03_eda_operations/) | Master | groupby, pivot tables, charts, 3 findings | pandas, matplotlib |
| 4 | [KPI dashboard in Power BI](04_kpi_dashboard_powerbi/) | Master | KPI csv and Power BI steps, no dashboard file | pandas, Power BI |
| 5 | [Statistics report](05_statistics_report/) | Master | descriptive stats, t-test, confidence interval, correlation | scipy, pandas |
| 6 | [Demand forecasting](06_demand_forecasting/) | Edge | naive baselines against Holt-Winters, MAPE | statsmodels |
| 7 | [Production mix optimizer](07_production_mix_optimizer/) | Edge | linear programming, finding the bottleneck | PuLP |
| 8 | [Inventory, EOQ and safety stock](08_inventory_eoq_safety_stock/) | Edge | EOQ, reorder point, safety stock, service level | math, scipy |
| 9 | [Predictive maintenance](09_predictive_maintenance/) | Edge | classifying machine failure, handling a rare class | scikit-learn |
| 10 | [Capstone, one operations story](10_capstone_operations_story/) | Both | template, numbers not filled | everything above |

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

BSc in Industrial Engineering and an MSc in Stochastics and Data Science at the University of Turin.

Eurix curricular internship on HVAC/AHU time series. The public repo ships a synthetic generator because the BMS extract is confidential.

Before that, industrial data monitoring and KPI dashboards for production managers.
