# Project 8, inventory, EOQ, safety stock and reorder point

Three classic inventory numbers for one part, plus what happens when you ask for a higher service level.

## How to run it

```
python inventory.py
```

## The three formulas and what they mean

EOQ is the square root of 2 times D times S over H. It is how much to order each time so that ordering cost plus holding cost is lowest.

Safety stock is z times the daily standard deviation times the square root of the lead time. It is the buffer for random demand spikes during the lead time.

Reorder point is daily demand times lead time, plus safety stock. When stock hits this number, I place a new order.

## Result for the sample part

Order 693 units each time, that is about 17 orders a year.

Keep 35 units of safety stock for a 95 percent service level.

Reorder when stock falls to 371 units.

Going from a 90 percent to a 99 percent service level takes the safety stock from 27 up to 49 units. That is the trade off a manager has to decide, fewer stock outs cost more inventory.

## Things I learned doing this

EOQ balances two costs that pull in opposite directions. Order often and the ordering cost is high, order big and the holding cost is high.

The z value comes from the normal distribution, 95 percent is about 1.65 and 99 percent is about 2.33.

Safety stock grows with the square root of the lead time, so a longer lead time hurts more than it looks.

