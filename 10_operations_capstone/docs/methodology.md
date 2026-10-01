# Methodology

SQL and pandas both use the cleaned tables.

Good units are `actual_qty - scrap_qty`. Attainment is `SUM(actual_qty) / SUM(planned_qty)` inside the group. A row-level average of ratios is not used, because a small shift would count as much as a large one.

The order gap is good units minus order units. Negative means production finished behind the orders.

The shift test takes total good units for each date and shift, then runs a Welch t-test. Welch does not assume the two shifts have the same spread.

The scrap interval is a 95% t interval for the mean of the daily scrap rates. Each day is one rate, scrap divided by actual. It is not a claim that every unit is an independent coin flip.

Downtime keeps one reason per row. Minutes are summed by that label. This is a screen, not a full loss tree.
