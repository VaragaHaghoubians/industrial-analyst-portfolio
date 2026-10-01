# Project brief

A supervisor asks one question: did this quarter's output cover the orders, and where did the time and scrap go?

The sample runs from 6 January 2025 for 90 days. Two shifts, three machines.

- PRESS_01 makes Bracket.
- WELD_01 makes Housing.
- LATHE_01 also makes Bracket and is given a higher scrap rate.

Morning plan is 100 units. Night plan is 80. Night downtime is drawn from a higher range. Weekly orders are about 8% above Bracket's good units and about 3% below Housing's good units, before rounding.

The database is built in memory from the CSVs each run. sqlite3 comes with Python.
