# Project brief

A maintenance lead asks whether yesterday's readings can flag a machine that fails today.

The sample has PRESS_01, WELD_01, LATHE_01 and PACK_01 for 180 days starting 1 January 2025. That is 720 rows. About 7.8% of the rows are failures.

The simulator makes a failure more likely when vibration, temperature and hours since maintenance are high. Pressure is recorded and is allowed as an input, but it does not create the label. That lets you see a coefficient that is not a cause.

Hours since maintenance reset to zero after a failure.
