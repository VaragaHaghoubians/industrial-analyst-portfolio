# Project 4, a production KPI dashboard in Python and Power BI

Power BI is click and drag, so the code part of this project is preparing a clean KPI dataset in Python. Then I build the dashboard on top of it with DAX measures and slicers.

## How to run it

```
python prepare_kpi_data.py
```

That creates kpi_data.csv, 120 days for 4 machines. Then I open Power BI Desktop and follow POWER_BI_STEPS.md, it has the exact DAX measures written out.

## The KPIs

Defect rate percent is defects divided by units made, times 100.

Uptime percent is planned minutes minus downtime, divided by planned minutes, times 100.

Good units is units made minus defects.

## Things I learned doing this

I calculate the raw KPIs in Python, but I make the measures in DAX, because a measure recalculates for whatever filter the manager clicks.

I use DIVIDE() instead of a plain slash in DAX, so a zero never crashes the dashboard.

Adding helper columns like month and weekday in Python gives me slicers for free.

## The dashboard

I will add dashboard.png here once I have built it in Power BI.

