# Validation

`python -m unittest discover -s tests -v` checks four things.

- The classic EOQ square root for demand 1,000, order cost 50 and holding cost 2.
- Ordering cost equals holding cost at that exact EOQ.
- Safety stock for a 4-week lead time is twice the 1-week safety stock, and the 95% z score is about 1.64485.
- Every "Reorder now" row has on-hand stock at or below its reorder point.

`src/main.py` also refuses negative demand, duplicate SKU-weeks, a holding rate outside 0 to 1, and a service level outside 0.5 to 1.

The published charts and `reports/metrics.json` come from seed 42. Change the seed only when you want a new sample, and say that you changed it.
