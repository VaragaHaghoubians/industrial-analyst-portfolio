# Start here

This project practices inventory math on fake warehouse data. Read it in this order.

1. Read the README and say what one weekly row means: one SKU, one week, one demand number.
2. Open `data/raw/sku_master.csv` and `data/raw/weekly_demand.csv`.
3. Run `src/main.py`. Read the printed action column before opening the charts.
4. Work through the notebooks in number order.
5. Recalculate the small example in `docs/kpi_examples.md` with a calculator.
6. Answer two questions in `docs/interview_questions.md` out loud.

A virtual environment is a separate folder for this project's libraries. The commands in the README call its Python directly.

## What each script does

| File | Simple explanation |
|---|---|
| src/generate_data.py | Builds eight SKUs and 52 weeks of demand with seed 42 |
| src/cleaning.py | Stops the run if a cost, demand or service level is impossible |
| src/inventory.py | Calculates EOQ, safety stock and the reorder point |
| src/visualization.py | Draws the cost curve, safety stock and stock versus reorder point |
| src/reporting.py | Writes the summary from the table |
| src/main.py | Runs these steps in order |

## Practice

- Change the on-hand value for BEARING in `src/generate_data.py` to 80 and run again. The action should leave "Reorder now".
- Change it back to 10 before you treat the published sample as the default.
- In the service-level curve, explain why 99% needs more stock per percentage point than 90%.

## Honest presentation

The lead time does not vary, and the demand is synthetic. Say that you can calculate the policy and explain the formula. Do not say this file is a live purchasing plan.
