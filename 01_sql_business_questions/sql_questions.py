# Project 01 - SQL business questions
# Goal: practice the SQL I need as an operations data analyst
# (JOIN, GROUP BY, window functions, CTE) on factory-style data.
#
# I use sqlite3 because it already comes with Python. No install needed.
# The script creates a small database, fills it with fake data, and then
# answers 5 business questions. Every answer is printed so I can read it.

import sqlite3
import random
from datetime import date, timedelta

random.seed(1)  # same random numbers every time, so results are repeatable

# ---------- step 1: connect (this creates factory.db if it is missing) ----------
conn = sqlite3.connect("factory.db")
cur = conn.cursor()

# start clean every run, otherwise the data doubles each time I run the script
cur.execute("DROP TABLE IF EXISTS production")
cur.execute("DROP TABLE IF EXISTS machines")

# ---------- step 2: create the tables ----------
cur.execute("""
CREATE TABLE machines (
    machine_id INTEGER PRIMARY KEY,
    machine_name TEXT,
    line TEXT
)
""")

cur.execute("""
CREATE TABLE production (
    prod_id INTEGER PRIMARY KEY AUTOINCREMENT,
    machine_id INTEGER,
    prod_date TEXT,      -- I store dates as text like 2026-01-15
    units_made INTEGER,
    defects INTEGER
)
""")

# ---------- step 3: put some fake data in ----------
machines = [
    (1, "Press A", "Line 1"),
    (2, "Press B", "Line 1"),
    (3, "Welder C", "Line 2"),
    (4, "Welder D", "Line 2"),
]
cur.executemany("INSERT INTO machines VALUES (?, ?, ?)", machines)

# 30 days of production for each machine
start = date(2026, 1, 1)
rows = []
for m_id, name, line in machines:
    for day in range(30):
        d = start + timedelta(days=day)
        units = random.randint(400, 600)
        # Welder D is my "bad" machine so the questions have something to find
        if m_id == 4:
            defects = random.randint(15, 40)
        else:
            defects = random.randint(2, 15)
        rows.append((m_id, d.isoformat(), units, defects))

cur.executemany(
    "INSERT INTO production (machine_id, prod_date, units_made, defects) VALUES (?, ?, ?, ?)",
    rows,
)
conn.commit()
print("Database ready with", len(rows), "production rows\n")


# small helper so I don't repeat the same print code 5 times
def show(title, query):
    print("=" * 60)
    print(title)
    print("=" * 60)
    for row in cur.execute(query):
        print(row)
    print()


# ---------- Q1: total units and defects per machine (JOIN + GROUP BY) ----------
show("Q1. Total units and defects per machine", """
SELECT m.machine_name,
       m.line,
       SUM(p.units_made) AS total_units,
       SUM(p.defects)    AS total_defects
FROM production p
JOIN machines m ON m.machine_id = p.machine_id
GROUP BY m.machine_name, m.line
ORDER BY total_units DESC
""")

# ---------- Q2: defect rate per machine, worst first ----------
# defect rate = defects / units. I multiply by 100.0 to get a percent.
# I write 100.0 (not 100) so SQLite does decimal division, not whole-number division.
show("Q2. Defect rate (%) per machine, worst first", """
SELECT m.machine_name,
       ROUND(100.0 * SUM(p.defects) / SUM(p.units_made), 2) AS defect_rate_pct
FROM production p
JOIN machines m ON m.machine_id = p.machine_id
GROUP BY m.machine_name
ORDER BY defect_rate_pct DESC
""")

# ---------- Q3: running total of units for one machine (WINDOW FUNCTION) ----------
# SUM(...) OVER (ORDER BY date) adds up the units day by day.
# This is what a "cumulative production" chart is built from.
show("Q3. Running total of units for Press A (first 10 days)", """
SELECT prod_date,
       units_made,
       SUM(units_made) OVER (ORDER BY prod_date) AS running_total
FROM production
WHERE machine_id = 1
ORDER BY prod_date
LIMIT 10
""")

# ---------- Q4: worst defect day per machine (CTE + ROW_NUMBER) ----------
# A CTE (the WITH ... part) is like a temporary table I can name and reuse.
# ROW_NUMBER gives each day a rank inside its own machine, 1 = most defects.
show("Q4. The single worst day for each machine", """
WITH ranked AS (
    SELECT machine_id,
           prod_date,
           defects,
           ROW_NUMBER() OVER (PARTITION BY machine_id ORDER BY defects DESC) AS rn
    FROM production
)
SELECT m.machine_name, r.prod_date, r.defects
FROM ranked r
JOIN machines m ON m.machine_id = r.machine_id
WHERE r.rn = 1
ORDER BY r.defects DESC
""")

# ---------- Q5: machines with a defect rate above the factory average (SUBQUERY) ----------
show("Q5. Machines worse than the factory average defect rate", """
SELECT m.machine_name,
       ROUND(100.0 * SUM(p.defects) / SUM(p.units_made), 2) AS defect_rate_pct
FROM production p
JOIN machines m ON m.machine_id = p.machine_id
GROUP BY m.machine_name
HAVING 1.0 * SUM(p.defects) / SUM(p.units_made) > (
    SELECT 1.0 * SUM(defects) / SUM(units_made) FROM production
)
""")

conn.close()
print("Done. (factory.db is left on disk so I can also open it in a SQL tool like DB Browser.)")
