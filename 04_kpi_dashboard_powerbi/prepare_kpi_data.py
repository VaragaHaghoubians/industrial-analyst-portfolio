# Project 04 - Preparing KPI data for a Power BI dashboard
# Power BI is a click-and-drag tool, so the "code" part of this project is
# preparing a clean, tidy csv with the KPIs a production manager wants:
# output, defect rate, downtime and uptime %.
# After running this, I open kpi_data.csv in Power BI and follow POWER_BI_STEPS.md

import pandas as pd
import numpy as np

np.random.seed(3)

days = pd.date_range("2026-01-01", periods=120, freq="D")
machines = ["Press A", "Press B", "Welder C", "Welder D"]
lines = {"Press A": "Line 1", "Press B": "Line 1", "Welder C": "Line 2", "Welder D": "Line 2"}
planned_minutes = 480  # one 8-hour shift

rows = []
for m in machines:
    for d in days:
        downtime = np.random.randint(0, 90)
        run_minutes = planned_minutes - downtime
        units = int(run_minutes * np.random.uniform(0.9, 1.3))  # roughly 1 unit per minute
        # Welder D is the weak machine, so its defect % is higher
        max_defect_share = 0.06 if m == "Welder D" else 0.03
        defects = int(units * np.random.uniform(0.01, max_defect_share))
        rows.append([d, m, lines[m], planned_minutes, downtime, units, defects])

df = pd.DataFrame(rows, columns=[
    "date", "machine", "line", "planned_minutes", "downtime_minutes", "units_made", "defects"
])

# ---------- the KPIs (I calculate them here so Power BI has less work) ----------
df["good_units"] = df["units_made"] - df["defects"]
df["defect_rate_pct"] = (df["defects"] / df["units_made"] * 100).round(2)
df["uptime_pct"] = ((df["planned_minutes"] - df["downtime_minutes"]) / df["planned_minutes"] * 100).round(2)

# helpful columns for slicers (filters) in Power BI
df["month"] = df["date"].dt.strftime("%Y-%m")
df["weekday"] = df["date"].dt.day_name()

df.to_csv("kpi_data.csv", index=False)
print("Saved kpi_data.csv with", len(df), "rows")
print(df.head())

print("\nQuick check of the KPIs per machine:")
print(df.groupby("machine")[["units_made", "defects", "defect_rate_pct", "uptime_pct"]].mean().round(2))
print("\nNext step: open kpi_data.csv in Power BI and follow POWER_BI_STEPS.md")
