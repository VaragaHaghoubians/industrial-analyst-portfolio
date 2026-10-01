# Data dictionary

One row in `machine_days.csv` is one machine on one day.

| Column | Meaning |
|---|---|
| date | Calendar day |
| machine_id | PRESS_01, WELD_01, LATHE_01 or PACK_01 |
| vibration_mm_s | Vibration reading |
| temperature_c | Temperature reading |
| pressure_bar | Pressure reading |
| hours_since_maintenance | Hours since the last failure in this sample |
| runtime_hours | Hours run that day |
| failure | 1 if the machine fails that day, otherwise 0 |

`failure` is the label. The other measurement columns are the model inputs, except `runtime_hours`, which is kept for context and is not in the model.
