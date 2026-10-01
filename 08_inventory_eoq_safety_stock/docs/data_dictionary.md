# Data dictionary

## sku_master.csv

| Column | Meaning |
|---|---|
| sku | Item code |
| category | Finished good or spare part |
| unit_cost | Purchase price of one unit, euro |
| order_cost | Cost of placing one order, euro |
| holding_rate | Yearly holding cost as a fraction of unit cost |
| lead_time_weeks | Supplier lead time, treated as constant |
| service_level | Chance of covering demand during the lead time |
| on_hand | Units in stock at the review |

## weekly_demand.csv

| Column | Meaning |
|---|---|
| sku | Item code |
| week | Week number, 1 to 52 |
| week_start | Monday of that week |
| demand_units | Units demanded that week |

One row is one SKU in one week. It is not one customer order.
