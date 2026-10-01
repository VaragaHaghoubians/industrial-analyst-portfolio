# Inventory policy summary

Synthetic demand for one year. These figures are calculated from the sample, not typed in as a result.

SKUs in the policy: 8.
Reorder now: BEARING, SEAL-KIT, HYDRAULIC-HOSE.
Stock is high and should be reviewed: SUPPORT.
Highest safety stock is BRACKET at 49.4 units.
Highest relevant order-and-hold cost is HOUSING at 1748.69 euro per year.
Total relevant cost across SKUs: 6795.77 euro per year.

Relevant cost here means ordering cost plus holding cost of the cycle stock. It does not include the purchase price of the parts.

## Policy table

| sku | order_qty | safety_stock | reorder_point | on_hand | action |
| --- | --- | --- | --- | --- | --- |
| BRACKET | 850 | 49.4 | 375.4 | 450 | Inside the band |
| HOUSING | 361 | 31.2 | 233.7 | 280 | Inside the band |
| SUPPORT | 314 | 19.2 | 97.5 | 520 | Stock is high, review |
| BEARING | 58 | 11.9 | 36.3 | 10 | Reorder now |
| FILTER | 94 | 10.5 | 29.8 | 50 | Inside the band |
| SEAL-KIT | 54 | 5.9 | 18.5 | 6 | Reorder now |
| WELD-TIP | 279 | 9.6 | 35.2 | 80 | Inside the band |
| HYDRAULIC-HOSE | 32 | 7.4 | 19.2 | 3 | Reorder now |

## Safety stock if the service level changes

The curve below uses the weekly variation and lead time of BRACKET. Each percentage point from 90% to 95% adds about 2.2 units. The single point from 98% to 99% adds about 8.2 units.

| service_level | safety_stock |
| --- | --- |
| 90% | 38.5 |
| 95% | 49.4 |
| 97% | 56.5 |
| 98% | 61.7 |
| 99% | 69.9 |

## How to explain the limitation

Lead time does not vary in this model. A late supplier would need a larger buffer than the table shows. Demand is also synthetic, so the actions are a method demo, not a purchasing decision.
