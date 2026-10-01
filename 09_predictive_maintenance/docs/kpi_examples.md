# Score examples you can do by hand

Suppose the test set has 100 days and 8 failures.

The baseline predicts no failure all 100 times.

- Accuracy is 92 / 100 = 92%.
- Recall is 0 / 8 = 0%.
- Precision is undefined in spirit, because there are no alarms. The code reports 0 with `zero_division=0`.

Now suppose the model flags 20 days, and 5 of those are real failures.

- Recall is 5 / 8 = 62.5%. It missed 3 failures.
- Precision is 5 / 20 = 25%. Fifteen alarms were false.
- Accuracy is the quiet days it got right, plus the 5 caught failures, divided by 100. It can be lower than 92% and still be the more useful model.

The published sample is the same idea: baseline accuracy 92.1% and recall 0%; model recall 64.7% and precision 25.6%.
