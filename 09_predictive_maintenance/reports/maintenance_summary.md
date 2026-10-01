# Predictive maintenance summary

Synthetic daily readings. The scores below come from one stratified holdout, not from a typed-in target.

Rows: 720. Failure rate: 7.8%.
Test failures: 17.
Always predicting no failure has accuracy 92.1% and recall 0.0%.
Balanced logistic regression has accuracy 82.4%, precision 25.6% and recall 64.7%.
After scaling, the largest coefficient is hours_since_maintenance (1.398).

A positive coefficient means a higher value raises the chance of a predicted failure. Precision says how many predicted failures were real. Recall says how many real failures were caught. A coefficient is not a cause. Pressure was not part of the failure rule, so its coefficient is only a fit to this sample.

## Coefficients

| feature | coefficient |
| --- | --- |
| hours_since_maintenance | 1.398 |
| vibration_mm_s | 0.723 |
| pressure_bar | 0.339 |
| temperature_c | 0.296 |

## How to explain the limitation

The split is random within the sample, so it is not a true future-week test. The failure rule was written into the simulator, which is why a simple model can find it. A real historian has sensor drift, maintenance notes and failures that do not follow a clean formula.
