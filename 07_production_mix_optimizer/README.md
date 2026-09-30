# Project 7, a production mix optimizer

This is the classic industrial engineering problem. We can make three products, but press hours, weld hours and steel are limited, so how many of each should we make this week to earn the most profit? I solve it in Python with PuLP.

## How to run it

```
pip install pulp
python optimize_mix.py
```

## Result on the sample data

Make 720 brackets, 20 frames, which is the customer order minimum, and 0 panels. Total profit is 9240 euro.

Press hours are used 400 out of 400, weld hours 174 out of 300, and steel 840 out of 1500. So the press is the bottleneck. Buying more press time would raise profit, buying more steel would change nothing.

## Things I learned doing this

A linear program is just three things, what I decide (the variables), what I want (the objective), and what I cannot break (the constraints).

The resource that is used 100 percent is the bottleneck, and that is the one worth investing in.

I set cat="Integer" because I cannot make half a frame.

Try it yourself, raise press_capacity at the top of the file and the profit goes up. Raise steel_available and nothing changes.

