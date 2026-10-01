# Operations Analytics Capstone — In Progress

## Business question

Which machines and shifts should an operations manager investigate first to address defects and production losses?

## Goal

Combine the SQL, data cleaning, exploratory analysis, statistics, and dashboard skills practised in Projects 1–5 into one operations analysis.

## Current status

The individual exercises are available in this repository. They generate separate synthetic datasets.

The integrated capstone, final management report, and Power BI dashboard are not yet complete.

## Planned workflow

1. **Create one shared dataset** containing production dates, machines, shifts, units produced, defects, and downtime.
2. **Use SQL** to summarize production and identify machines with higher defect rates.
3. **Clean and explore the data with pandas**, documenting data-quality issues and comparing machines and shifts.
4. **Evaluate the differences statistically**, reporting their size and uncertainty and checking the assumptions of the chosen method.
5. **Build a Power BI dashboard** with production, defect-rate, and downtime measures and filters.
6. **Write a management summary** with findings, limitations, and recommended investigations.

Defect rates will be calculated as total defects divided by total units produced for each group.

## Planned deliverables

- Shared synthetic dataset
- SQL queries and Python analysis
- Power BI dashboard and screenshot
- One-page management summary

## Data and limitations

This is a learning project using synthetic manufacturing data. Recommendations will illustrate how an analyst prioritizes investigations; they will not represent verified improvements at a real factory.

Results will be added after the integrated analysis is completed and checked.
