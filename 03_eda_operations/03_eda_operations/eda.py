# Project 03 - Exploratory Data Analysis (EDA) on operations data
# EDA = looking at the data properly before doing anything clever with it.
# I want to end with 3 clear findings a production manager would care about.
# The script makes its own data so it runs anywhere.

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")  # lets me save charts to files without a window popping up
import matplotlib.pyplot as plt

np.random.seed(2)

# ---------- step 1: build a daily production table ----------
days = pd.date_range("2026-01-01", periods=90, freq="D")
machines = ["Press A", "Press B", "Welder C", "Welder D"]
rows = []
for m in machines:
    for d in days:
        units = np.random.randint(400, 600)
        # Welder D is the weak machine, and night shift has more defects
        base_defects = 25 if m == "Welder D" else 8
        shift = np.random.choice(["Morning", "Evening", "Night"])
        extra = 6 if shift == "Night" else 0
        defects = max(0, int(np.random.normal(base_defects + extra, 4)))
        downtime = np.random.randint(0, 60)  # minutes
        rows.append([d, m, shift, units, defects, downtime])

df = pd.DataFrame(rows, columns=["date", "machine", "shift", "units", "defects", "downtime_min"])
df["defect_rate"] = df["defects"] / df["units"] * 100
print("Data shape:", df.shape)
print(df.head(), "\n")

# ---------- step 2: quick overall numbers ----------
print("--- describe() gives me min / max / mean in one go ---")
print(df[["units", "defects", "downtime_min", "defect_rate"]].describe().round(2), "\n")

# ---------- step 3: group by machine ----------
by_machine = df.groupby("machine").agg(
    total_units=("units", "sum"),
    total_defects=("defects", "sum"),
    avg_defect_rate=("defect_rate", "mean"),
    avg_downtime=("downtime_min", "mean"),
).round(2)
print("--- per machine ---")
print(by_machine, "\n")

# ---------- step 4: pivot table: machine vs shift ----------
pivot = df.pivot_table(values="defect_rate", index="machine", columns="shift", aggfunc="mean").round(2)
print("--- average defect rate (%) by machine and shift ---")
print(pivot, "\n")

# ---------- step 5: charts (saved as png files) ----------
# chart 1: defect rate per machine
by_machine["avg_defect_rate"].plot(kind="bar", title="Average defect rate (%) per machine")
plt.ylabel("%")
plt.tight_layout()
plt.savefig("chart_defect_rate_by_machine.png")
plt.close()

# chart 2: daily total units over time
daily = df.groupby("date")["units"].sum()
daily.plot(title="Total units per day (all machines)")
plt.ylabel("units")
plt.tight_layout()
plt.savefig("chart_units_over_time.png")
plt.close()

# chart 3: does downtime relate to defects? (scatter)
plt.scatter(df["downtime_min"], df["defect_rate"], alpha=0.4)
plt.xlabel("downtime (minutes)")
plt.ylabel("defect rate (%)")
plt.title("Downtime vs defect rate")
plt.tight_layout()
plt.savefig("chart_downtime_vs_defects.png")
plt.close()
print("Saved 3 charts as png files.\n")

# ---------- step 6: my 3 findings (written as text so they are easy to read) ----------
worst = by_machine["avg_defect_rate"].idxmax()
worst_rate = by_machine.loc[worst, "avg_defect_rate"]
night_rate = df[df["shift"] == "Night"]["defect_rate"].mean()
day_rate = df[df["shift"] != "Night"]["defect_rate"].mean()
corr = df["downtime_min"].corr(df["defect_rate"])

print("=== MY 3 FINDINGS ===")
print(f"1. {worst} has the highest defect rate ({worst_rate:.2f}%). It should be checked first.")
print(f"2. Night shift defect rate is {night_rate:.2f}% vs {day_rate:.2f}% on the other shifts.")
print(f"3. Correlation between downtime and defect rate is {corr:.2f} "
      f"({'weak' if abs(corr) < 0.3 else 'noticeable'}) - downtime does not explain the defects here.")
