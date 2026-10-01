# Start here

This is the capstone. It uses SQL, pandas, a statistical test and a Power BI extract on one story.

1. Read the README. One production row is one machine on one shift of one day.
2. Run `src/main.py`.
3. Open `data/processed/orders_against_good_units.csv` and say which product is behind.
4. Work through notebooks 01, 02 and 03. Notebook 04 points at the written summary.
5. Follow `dashboard/POWER_BI_STEPS.md` if Power BI Desktop is installed.
6. Practice two interview questions. Include one limitation in the answer.

## What each script does

| File | Simple explanation |
|---|---|
| src/generate_data.py | Builds 90 days of production and weekly orders with seed 42 |
| src/cleaning.py | Checks that scrap cannot exceed actual, and actual cannot exceed the plan |
| src/sql_questions.py | Answers four questions in sqlite |
| src/kpi.py | Calculates the same operations measures in pandas |
| src/shift_stats.py | Compares shifts and builds a scrap-rate interval |
| src/visualization.py | Draws attainment, scrap and downtime |
| src/reporting.py | Writes the summary from those results |
| src/main.py | Runs these steps in order |

## Practice

Name the product that is behind orders, the shift with lower attainment, and the downtime reason with the most minutes. Then say why the small p-value does not prove that night shift causes the loss.

## Honest presentation

Each production row keeps one downtime reason. A shift with two problems is stored as one bucket. Say that when you show the Pareto.
