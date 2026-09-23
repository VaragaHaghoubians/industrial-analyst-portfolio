# Power BI steps for the KPI dashboard

I run prepare_kpi_data.py first, it creates kpi_data.csv. Then I do the steps below in Power BI Desktop, which is free, just search "Power BI Desktop" in the Microsoft Store.

## 1. Load the data

Go to Home, then Get Data, then Text/CSV, choose kpi_data.csv and click Load.

Check that the date column is a Date type. In Table view click the column and set the Data type to Date.

## 2. Make the measures in DAX

Right click the kpi_data table and choose New measure. Add these one at a time:

```
Total Units = SUM(kpi_data[units_made])

Total Defects = SUM(kpi_data[defects])

Defect Rate % = DIVIDE([Total Defects], [Total Units]) * 100

Total Downtime (min) = SUM(kpi_data[downtime_minutes])

Uptime % = DIVIDE(SUM(kpi_data[planned_minutes]) - [Total Downtime (min)], SUM(kpi_data[planned_minutes])) * 100
```

Why measures and not normal columns? A measure recalculates itself for whatever filter is on, one machine, one month, one line. A column is fixed per row. Managers click filters all the time, so measures are the right tool.

I use DIVIDE instead of a plain slash because DIVIDE does not crash when the bottom number is zero.

## 3. Build the page

Four cards across the top, Total Units, Defect Rate %, Uptime % and Total Downtime (min).

A line chart with date on the X axis and Total Units on the Y axis, this shows the production trend.

A clustered bar chart with machine on the axis and Defect Rate % as the value, sorted descending so the worst machine is first.

A matrix with machine as rows, month as columns and Uptime % as the value.

Slicers for line, machine and month.

## 4. Make it readable

Format Defect Rate % and Uptime % to one decimal place.

Give it a title, "Production KPIs, January to April 2026".

Put a conditional colour on the defect rate bars so high is red.

## 5. Save and show

Save it as kpi_dashboard.pbix in this folder.

Take a screenshot and save it as dashboard.png so it shows in the README on GitHub.

