# Data dictionary

## production.csv

| Column | Meaning |
|---|---|
| date | Production day |
| shift | Morning or Night |
| machine_id | PRESS_01, WELD_01 or LATHE_01 |
| product | Bracket or Housing |
| planned_qty | Units planned for that shift |
| actual_qty | Units made, never above the plan |
| scrap_qty | Scrapped units, never above actual |
| downtime_min | Lost minutes |
| reason | One label: Breakdown, Setup or Material wait |

Good quantity is actual minus scrap. It is calculated later. It is not a raw column.

## orders.csv

| Column | Meaning |
|---|---|
| order_id | One row per product per week |
| week_start | Week starting Monday-aligned period start |
| product | Bracket or Housing |
| order_qty | Units ordered that week |

## kpi_data.csv

The production rows plus `good_qty`, saved for Power BI.
