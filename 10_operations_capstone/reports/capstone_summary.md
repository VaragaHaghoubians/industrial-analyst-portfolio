# Operations capstone summary

One synthetic quarter. SQL, pandas and the statistical test use the same tables.

Bracket finished 2342 good units behind orders.
Largest downtime reason: Breakdown (10220 minutes).
Attainment is 96.3% in the morning and 89.4% at night.
Mean daily good units are 281.8 in the morning and 208.5 at night. The Welch t-test p-value is < 0.0001.
Mean daily scrap rate is 2.61%, with a 95% interval from 2.60% to 2.63%. The interval is narrow because the daily scrap rate barely moves in this sample.

## Orders against good units

| product | order_qty | good_qty | gap |
| --- | --- | --- | --- |
| Bracket | 31614 | 29272 | -2342 |
| Housing | 14412 | 14860 | 448 |

## How to explain the limitation

The night shift was given more downtime in the simulator, so a small p-value shows that the sample preserves that pattern. It does not prove a cause in a real plant. Each row also keeps one downtime reason, so a shift with two problems is recorded as the larger bucket only.
