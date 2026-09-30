# Project 07 - Production mix optimizer (linear programming)
# Classic industrial engineering question: we can make 3 products, but machine
# time and raw material are limited. How many of each should we make to earn
# the most profit? I solve it with PuLP (pip install pulp).
# This is the same maths I learned in my IE degree, now in Python.

try:
    import pulp
except ImportError:
    print("Please run: pip install pulp")
    raise

# ---------- step 1: the data (per ONE unit of each product) ----------
products = ["Bracket", "Frame", "Panel"]
profit = {"Bracket": 12, "Frame": 30, "Panel": 20}          # euro per unit
press_hours = {"Bracket": 0.5, "Frame": 2.0, "Panel": 1.0}   # hours on the press
weld_hours = {"Bracket": 0.2, "Frame": 1.5, "Panel": 0.8}    # hours on the welder
steel_kg = {"Bracket": 1, "Frame": 6, "Panel": 3}            # kg of steel

# ---------- step 2: what is available this week ----------
press_capacity = 400    # hours
weld_capacity = 300     # hours
steel_available = 1500  # kg
min_frames = 20         # a customer already ordered 20 frames, so I must make at least 20

# ---------- step 3: build the model ----------
model = pulp.LpProblem("weekly_production_mix", pulp.LpMaximize)

# decision variables = how many of each product to make (whole numbers, never negative)
make = {p: pulp.LpVariable(f"make_{p}", lowBound=0, cat="Integer") for p in products}

# objective = total profit (this is the thing I want to maximise)
model += pulp.lpSum(profit[p] * make[p] for p in products), "total_profit"

# constraints = the limits I cannot break
model += pulp.lpSum(press_hours[p] * make[p] for p in products) <= press_capacity, "press_hours"
model += pulp.lpSum(weld_hours[p] * make[p] for p in products) <= weld_capacity, "weld_hours"
model += pulp.lpSum(steel_kg[p] * make[p] for p in products) <= steel_available, "steel"
model += make["Frame"] >= min_frames, "customer_order"

# ---------- step 4: solve ----------
model.solve(pulp.PULP_CBC_CMD(msg=0))   # msg=0 hides the solver's long log
print("Status:", pulp.LpStatus[model.status])
print()

# ---------- step 5: read the answer ----------
print("=== Best production plan for the week ===")
for p in products:
    print(f"{p:8s}: make {int(make[p].value())} units")
print(f"\nTotal profit: {pulp.value(model.objective):.0f} euro")

# ---------- step 6: which limits are actually binding? ----------
# If a resource is fully used, that is the bottleneck. Buying more of it would raise profit.
print("\n=== Resource usage ===")
used_press = sum(press_hours[p] * make[p].value() for p in products)
used_weld = sum(weld_hours[p] * make[p].value() for p in products)
used_steel = sum(steel_kg[p] * make[p].value() for p in products)
print(f"Press hours: {used_press:.1f} / {press_capacity}")
print(f"Weld hours : {used_weld:.1f} / {weld_capacity}")
print(f"Steel (kg) : {used_steel:.1f} / {steel_available}")
print("\nThe resource closest to its limit is the bottleneck of this factory.")
print("Try it: raise that limit at the top of the file and run again - profit should go up.")
