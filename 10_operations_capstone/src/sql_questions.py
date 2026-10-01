"""Four SQL questions on the capstone tables.

sqlite3 comes with Python. The database is built in memory from the CSVs,
so a rerun does not stack old rows on top of new ones.
"""

import sqlite3

import pandas as pd

QUESTIONS = {
    "good_units_by_product": """
        SELECT product,
               SUM(actual_qty - scrap_qty) AS good_qty
        FROM production
        GROUP BY product
        ORDER BY good_qty DESC
    """,
    "attainment_by_shift": """
        SELECT shift,
               ROUND(SUM(actual_qty) * 1.0 / SUM(planned_qty), 4) AS attainment
        FROM production
        GROUP BY shift
        ORDER BY shift
    """,
    "downtime_by_reason": """
        SELECT reason,
               SUM(downtime_min) AS downtime_min
        FROM production
        GROUP BY reason
        ORDER BY downtime_min DESC
    """,
    "orders_against_good_units": """
        WITH produced AS (
            SELECT product, SUM(actual_qty - scrap_qty) AS good_qty
            FROM production
            GROUP BY product
        ),
        ordered AS (
            SELECT product, SUM(order_qty) AS order_qty
            FROM orders
            GROUP BY product
        )
        SELECT ordered.product,
               ordered.order_qty,
               produced.good_qty,
               produced.good_qty - ordered.order_qty AS gap
        FROM ordered
        JOIN produced ON produced.product = ordered.product
        ORDER BY gap
    """,
}


def connect(production: pd.DataFrame, orders: pd.DataFrame) -> sqlite3.Connection:
    connection = sqlite3.connect(":memory:")
    production_out = production.copy()
    orders_out = orders.copy()
    production_out["date"] = pd.to_datetime(production_out["date"]).dt.strftime("%Y-%m-%d")
    orders_out["week_start"] = pd.to_datetime(orders_out["week_start"]).dt.strftime("%Y-%m-%d")
    production_out.to_sql("production", connection, index=False)
    orders_out.to_sql("orders", connection, index=False)
    return connection


def run_questions(production: pd.DataFrame, orders: pd.DataFrame) -> dict[str, pd.DataFrame]:
    connection = connect(production, orders)
    try:
        return {
            name: pd.read_sql_query(query, connection)
            for name, query in QUESTIONS.items()
        }
    finally:
        connection.close()
