# Methodology

Annual demand is the sum of the 52 weekly demands.

Holding cost per unit per year is unit cost times the holding rate.

EOQ is the square root of `2 × annual demand × order cost / holding cost per unit`. The recommended order quantity is that value rounded to the nearest unit.

Weekly mean and weekly standard deviation use the 52 observed weeks. The standard deviation divides by 51, which is the sample version.

Lead-time demand is weekly mean times lead time in weeks.

Safety stock is `z × weekly standard deviation × square root of lead time`. `z` comes from the normal table at the chosen service level. This assumes independent weeks and a lead time that does not change.

Reorder point is lead-time demand plus safety stock.

Actions:

- Reorder now: on hand is at or below the reorder point.
- Inside the band: on hand is above the reorder point and within one order quantity of it.
- Stock is high, review: on hand is above the reorder point plus one order quantity.

Relevant cost is the ordering cost plus the holding cost of cycle stock at the rounded order quantity. It excludes the purchase price.
