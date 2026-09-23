# Project 06 - Demand forecasting
# Rule I learned: ALWAYS compare against a simple baseline. A fancy model that
# cannot beat "same as last month" is useless.
# I compare: naive, seasonal naive, moving average, and Holt-Winters.
# I score them with MAPE (mean absolute percentage error). Lower is better.

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

try:
    from statsmodels.tsa.holtwinters import ExponentialSmoothing
except ImportError:
    print("Please run: pip install statsmodels")
    raise

np.random.seed(5)

# ---------- step 1: make 4 years of monthly demand with trend + seasonality ----------
months = pd.date_range("2022-01-01", periods=48, freq="MS")
trend = np.linspace(1000, 1400, 48)                       # slowly growing
season = 150 * np.sin(2 * np.pi * np.arange(48) / 12)     # yearly wave (summer high, winter low)
noise = np.random.normal(0, 40, 48)
demand = pd.Series(trend + season + noise, index=months).round()

# ---------- step 2: split. The last 12 months are the "future" I pretend not to know ----------
# IMPORTANT: for time series I never shuffle. The past predicts the future, not the other way round.
train = demand[:-12]
test = demand[-12:]


def mape(actual, forecast):
    # average of |actual - forecast| / actual, as a percent
    actual = np.asarray(actual, dtype=float)
    forecast = np.asarray(forecast, dtype=float)
    return float(np.mean(np.abs((actual - forecast) / actual)) * 100)


results = {}

# ---------- model 1: naive - "next month = the last month I saw" ----------
naive = pd.Series(train.iloc[-1], index=test.index)
results["Naive"] = mape(test, naive)

# ---------- model 2: seasonal naive - "same month last year" ----------
seasonal_naive = pd.Series(train.iloc[-12:].values, index=test.index)
results["Seasonal naive"] = mape(test, seasonal_naive)

# ---------- model 3: moving average of the last 3 months ----------
moving_avg = pd.Series(train.iloc[-3:].mean(), index=test.index)
results["Moving average (3)"] = mape(test, moving_avg)

# ---------- model 4: Holt-Winters (handles trend AND seasonality) ----------
model = ExponentialSmoothing(train, trend="add", seasonal="add", seasonal_periods=12).fit()
holt_winters = model.forecast(12)
results["Holt-Winters"] = mape(test, holt_winters)

# ---------- step 3: compare ----------
print("=== MAPE on the 12 test months (lower is better) ===")
for name, score in sorted(results.items(), key=lambda x: x[1]):
    print(f"{name:20s} {score:6.2f}%")
best = min(results, key=results.get)
print(f"\nBest model: {best}")
print("If the fancy model did not beat seasonal naive, I would not trust it.")

# ---------- step 4: chart ----------
plt.figure(figsize=(10, 5))
plt.plot(train.index, train.values, label="train (history)")
plt.plot(test.index, test.values, label="actual (test)", color="black")
plt.plot(test.index, seasonal_naive.values, "--", label="seasonal naive")
plt.plot(test.index, np.asarray(holt_winters), "--", label="Holt-Winters")
plt.title("Monthly demand forecast")
plt.legend()
plt.tight_layout()
plt.savefig("forecast_chart.png")
plt.close()
print("Saved forecast_chart.png")

# save the forecast so it can go into Power BI or Excel
out = pd.DataFrame({
    "actual": test.values,
    "seasonal_naive": seasonal_naive.values,
    "holt_winters": np.asarray(holt_winters),
}, index=test.index).round(0)
out.to_csv("forecast_results.csv")
print("Saved forecast_results.csv")
