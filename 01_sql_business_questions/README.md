# Project 1, SQL business questions

This is my first project. I wanted to practice the SQL that shows up in every data analyst job posting, so I built a tiny factory database with 4 machines and 30 days of production, and then answered 5 questions a plant manager would actually ask.

The SQL ideas in here are JOIN, GROUP BY, a window function for a running total, a CTE with ROW_NUMBER, and a subquery inside HAVING.

## How to run it

```
python sql_questions.py
```

Nothing to install; sqlite3 comes with Python. The script creates factory.db, fills it with sample data, and prints every answer.

## What the questions are

Q1 is the total units and defects for each machine.

Q2 is the defect rate as a percent, with the worst machine first.

Q3 is a running total of production for one machine; that is the window function.

Q4 finds the single worst day for each machine, using a CTE and ROW_NUMBER.

Q5 finds the machines above the factory average defect rate. In the sample data, only Welder D shows up, at 5.28 percent.

## Things I learned doing this

I have to write 100.0 and not 100; otherwise, SQLite does whole-number division, and the defect rate comes out as 0.

A window function like SUM(...) OVER (ORDER BY date) gives me a running total without a messy self join.

A CTE, the WITH ranked AS part, turns a two-step question into something I can actually read.

I drop and recreate the tables at the start, because otherwise the data doubles every time I run the script.

