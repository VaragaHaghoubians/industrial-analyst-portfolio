# Project 08 - Inventory: EOQ, safety stock and reorder point
# Three classic supply-chain formulas every operations analyst should know.
# I put the formula AND the plain-English meaning next to each other so I
# never forget what they are for. Only math and scipy (for the z value) needed.

import math

try:
    from scipy.stats import norm
except ImportError:
    print("Please run: pip install scipy")
    raise

# ---------- inputs for one part (steel brackets) ----------
annual_demand = 12000        # units per year
order_cost = 50              # euro every time I place an order (admin, shipping...)
holding_cost = 2.5           # euro to keep ONE unit in stock for a whole year
lead_time_days = 7           # days between placing the order and receiving it
working_days = 250
daily_demand_std = 8         # how much daily demand jumps around (standard deviation)
service_level = 0.95         # I want to avoid a stock-out 95% of the time

daily_demand = annual_demand / working_days

# ---------- 1. EOQ - Economic Order Quantity ----------
# "How much should I order each time so ordering cost + holding cost together is lowest?"
# formula: sqrt( 2 * D * S / H )
eoq = math.sqrt(2 * annual_demand * order_cost / holding_cost)
orders_per_year = annual_demand / eoq
total_cost = (annual_demand / eoq) * order_cost + (eoq / 2) * holding_cost

print("=== 1. EOQ ===")
print(f"Order {eoq:.0f} units each time.")
print(f"That means about {orders_per_year:.1f} orders per year.")
print(f"Yearly ordering + holding cost at EOQ: {total_cost:.0f} euro\n")

# ---------- 2. Safety stock ----------
# "Extra stock I keep so random spikes in demand during the lead time don't leave me empty."
# formula: z * sigma_daily * sqrt(lead_time)
# z comes from the normal distribution. 95% service level -> z is about 1.65
z = norm.ppf(service_level)
safety_stock = z * daily_demand_std * math.sqrt(lead_time_days)

print("=== 2. Safety stock ===")
print(f"z for {service_level:.0%} service level = {z:.2f}")
print(f"Safety stock = {safety_stock:.0f} units\n")

# ---------- 3. Reorder point ----------
# "When stock drops to this number, place a new order."
# formula: (daily demand * lead time) + safety stock
reorder_point = daily_demand * lead_time_days + safety_stock

print("=== 3. Reorder point ===")
print(f"Daily demand = {daily_demand:.1f} units")
print(f"Demand during lead time = {daily_demand * lead_time_days:.0f} units")
print(f"Reorder point = {reorder_point:.0f} units\n")

# ---------- summary a manager could read ----------
print("=== Summary for the manager ===")
print(f"Every time stock of brackets falls to {reorder_point:.0f} units, order {eoq:.0f} more.")
print(f"Keep {safety_stock:.0f} units as a safety buffer.")
print("This balances ordering cost, holding cost and the risk of running out.")

# ---------- little experiment: what if I want a higher service level? ----------
print("\n=== What if I want a higher service level? ===")
for sl in [0.90, 0.95, 0.99]:
    ss = norm.ppf(sl) * daily_demand_std * math.sqrt(lead_time_days)
    print(f"{sl:.0%} service level -> safety stock {ss:.0f} units")
print("Higher service level = a lot more safety stock. That is the trade-off managers must decide.")
