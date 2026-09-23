# Project 5, statistics I can actually explain

This project answers one real question with numbers and with plain English. Does Welder D really make more defects than Welder C, or is it just noise?

I use descriptive statistics, a 95 percent confidence interval, a two sample t-test and a Pearson correlation, all with scipy.

## How to run it

```
python stats_report.py
```

It prints the analysis and saves stats_summary.csv.

## What the results say, on the sample data

Welder C makes about 10.1 defects a day and Welder D about 14.3, and the two 95 percent confidence intervals do not overlap.

The t-test gives p below 0.05, so the difference is statistically significant, it is not random noise.

Machine speed against defects has a Pearson r of about 0.61, so running faster comes with more defects.

## Things I learned doing this

A confidence interval is the range I would expect the true mean to sit in. If two intervals do not overlap, that is already a strong hint.

The t-test gives a p-value, and below 0.05 I reject the idea that the machines are the same.

Correlation is not cause. Speed goes with defects, but I would still test it on the line before changing anything.

Every result needs a plain English sentence, otherwise the manager cannot use it.

