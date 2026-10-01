# Formula examples you can do by hand

These examples are small on purpose. They are not the eight-SKU sample.

## EOQ

Annual demand 1,000. Order cost 50 euro. Holding cost 2 euro per unit per year.

`EOQ = sqrt(2 × 1000 × 50 / 2) = sqrt(50,000) = 223.61` units.

At that quantity, ordering cost and cycle-stock holding cost are equal. The test `test_order_and_hold_costs_meet_at_the_eoq` checks this.

## Safety stock

Weekly standard deviation 10 units. Lead time 4 weeks. Service level 95%, so z is about 1.645.

`Safety stock = 1.645 × 10 × sqrt(4) = 32.9` units.

Doubling the lead time from 1 week to 4 weeks doubles the safety stock, because the square root of 4 is 2. It does not multiply the buffer by 4.

## Reorder point

If average weekly demand is 20 and the lead time is 4 weeks, expected lead-time demand is 80. Add the 32.9 safety stock and the reorder point is 112.9 units.
