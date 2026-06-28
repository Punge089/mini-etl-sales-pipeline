"""SQL query module for analytics."""

from pathlib import Path
import sqlite3
import pandas as pd


def run_query(database_path: str | Path, query: str) -> pd.DataFrame:
    """Run a SQL query against the SQLite database."""
    with sqlite3.connect(database_path) as conn:
        return pd.read_sql_query(query, conn)


def get_business_metrics(database_path: str | Path) -> dict[str, pd.DataFrame]:
    """Generate SQL-based business metrics from the sales table."""
    queries = {
        "total_revenue": """
            SELECT ROUND(SUM(revenue), 2) AS total_revenue
            FROM sales;
        """,
        "monthly_revenue": """
            SELECT order_month, ROUND(SUM(revenue), 2) AS monthly_revenue
            FROM sales
            GROUP BY order_month
            ORDER BY order_month;
        """,
        "top_products": """
            SELECT product, ROUND(SUM(revenue), 2) AS total_revenue
            FROM sales
            GROUP BY product
            ORDER BY total_revenue DESC
            LIMIT 5;
        """,
        "region_revenue": """
            SELECT region, ROUND(SUM(revenue), 2) AS total_revenue
            FROM sales
            GROUP BY region
            ORDER BY total_revenue DESC;
        """,
        "average_order_value": """
            SELECT ROUND(AVG(revenue), 2) AS average_order_value
            FROM sales;
        """,
    }

    return {name: run_query(database_path, sql) for name, sql in queries.items()}
