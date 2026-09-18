# Project 05 - Statistics I can explain
# The point of this project is not fancy maths. It is answering a real question
# with numbers AND saying what the numbers mean in plain English.
# Question: does Welder D really make more defects than Welder C, or is it just noise?

import numpy as np
import pandas as pd
from scipy import stats

np.random.seed(4)

# ---------- step 1: 60 days of defects for two machines ----------
welder_c = np.random.normal(loc=10, scale=3, size=60).round().clip(0)
welder_d = np.random.normal(loc=14, scale=3, size=60).round().clip(0)

# ---------- step 2: descriptive statistics ----------
print("=== Descriptive statistics (defects per day) ===")
for name, data in [("Welder C", welder_c), ("Welder D", welder_d)]:
    print(f"{name}: mean={data.mean():.2f}  median={np.median(data):.1f}  "
          f"std={data.std(ddof=1):.2f}  min={data.min():.0f}  max={data.max():.0f}")
print()

# ---------- step 3: 95% confidence interval for each mean ----------
# Plain English: "if I repeated this 100 times, about 95 of the intervals would contain the true mean."
print("=== 95% confidence intervals for the mean ===")
for name, data in [("Welder C", welder_c), ("Welder D", welder_d)]:
    n = len(data)
    mean = data.mean()
    sem = data.std(ddof=1) / np.sqrt(n)          # standard error of the mean
    low, high = stats.t.interval(0.95, df=n - 1, loc=mean, scale=sem)
    print(f"{name}: {mean:.2f}  (95% CI: {low:.2f} to {high:.2f})")
print("If the two intervals do not overlap, that is already a strong hint the machines differ.\n")

# ---------- step 4: hypothesis test (two-sample t-test) ----------
# H0 (null): the two machines have the SAME average defects
# H1: they are DIFFERENT
# If the p-value is below 0.05, I reject H0 and say the difference is real.
t_stat, p_value = stats.ttest_ind(welder_c, welder_d)
print("=== Two-sample t-test ===")
print(f"t = {t_stat:.3f},  p-value = {p_value:.4f}")
if p_value < 0.05:
    print("-> p < 0.05, so the difference is statistically significant.")
    print("   Welder D really does produce more defects. It is not just random noise.")
else:
    print("-> p >= 0.05, so I cannot say the machines are different with this data.")
print()

# ---------- step 5: correlation - does machine speed relate to defects? ----------
speed = np.random.uniform(80, 120, 60)                        # units per hour
defects_by_speed = 5 + 0.12 * speed + np.random.normal(0, 2, 60)
r, p_corr = stats.pearsonr(speed, defects_by_speed)
print("=== Correlation between speed and defects ===")
print(f"Pearson r = {r:.2f}  (p-value {p_corr:.4f})")
if abs(r) > 0.5:
    print("-> Strong relationship: running the machine faster comes with more defects.")
elif abs(r) > 0.3:
    print("-> Moderate relationship between speed and defects.")
else:
    print("-> Weak or no relationship.")
print("   Reminder to self: correlation is not proof of cause. I would still test it on the line.")

# ---------- step 6: save a small report table ----------
report = pd.DataFrame({
    "machine": ["Welder C", "Welder D"],
    "mean_defects": [welder_c.mean(), welder_d.mean()],
    "std": [welder_c.std(ddof=1), welder_d.std(ddof=1)],
}).round(2)
report.to_csv("stats_summary.csv", index=False)
print("\nSaved stats_summary.csv")
