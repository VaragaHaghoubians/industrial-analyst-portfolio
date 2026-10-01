# Power BI steps

Power BI Desktop is free. Search for it in the Microsoft Store. Run `src/main.py` before these steps so `data/processed/kpi_data.csv` exists.

## 1. Load the data

Home, Get Data, Text/CSV, then choose `kpi_data.csv` and Load.

In Table view, set `date` to the Date type.

## 2. Measures

Right-click the table and choose New measure. Add these one at a time.

```
Good Units = SUM(kpi_data[good_qty])

Planned Units = SUM(kpi_data[planned_qty])

Actual Units = SUM(kpi_data[actual_qty])

Attainment % = DIVIDE([Actual Units], [Planned Units])

Scrap % = DIVIDE(SUM(kpi_data[scrap_qty]), [Actual Units])

Downtime Minutes = SUM(kpi_data[downtime_min])
```

`DIVIDE` stays blank instead of breaking when a filter has no rows.

## 3. Page

Four cards: Good Units, Attainment %, Scrap %, Downtime Minutes.

A line chart with `date` on the axis and Good Units as the value.

A bar chart with `machine_id` and Scrap %.

A bar chart with `reason` and Downtime Minutes.

A slicer for `shift`.

Morning attainment in the published file is 96.3%. Night is 89.4%. If the slicer does not move those cards, the measure is not using `DIVIDE` of the summed columns.
