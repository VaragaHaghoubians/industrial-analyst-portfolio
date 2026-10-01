# Validation

`python -m unittest discover -s tests -v` checks three things.

- Good units by product match between SQL and pandas.
- Morning attainment from SQL equals the sum of actual divided by the sum of planned.
- Morning mean good units are higher than night, the p-value is between 0 and 1, and the scrap interval sits around the mean.

Cleaning rejects actual above plan, scrap above actual, and a zero plan. The published files use seed 42.
