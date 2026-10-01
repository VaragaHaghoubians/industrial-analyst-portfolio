# Validation

`python -m unittest discover -s tests -v` checks two things.

- The failure rate is between 2% and 15%, and the label is not a model input.
- The baseline recall is 0, the test set contains at least one failure, and the balanced model recall is higher than the baseline.

The published scores in `reports/metrics.json` come from seed 42 and a 30% stratified split. They will change if the seed or the split changes. Say so if you change either one.
