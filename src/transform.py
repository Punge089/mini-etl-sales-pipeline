"""Transform module for cleaning and preparing sales data."""

import pandas as pd


def clean_sales_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean raw sales data and calculate revenue.

    Cleaning steps:
    - Standardize column names
    - Remove duplicate rows
    - Convert date and numeric columns
    - Handle missing values
    - Remove invalid records
    - Create revenue and month columns

    Args:
        df: Raw sales DataFrame.

    Returns:
        Cleaned sales DataFrame.
    """
    cleaned = df.copy()
    cleaned.columns = [col.strip().lower() for col in cleaned.columns]
    cleaned = cleaned.drop_duplicates()

    cleaned["order_date"] = pd.to_datetime(cleaned["order_date"], errors="coerce")
    cleaned["quantity"] = pd.to_numeric(cleaned["quantity"], errors="coerce")
    cleaned["unit_price"] = pd.to_numeric(cleaned["unit_price"], errors="coerce")

    cleaned["quantity"] = cleaned["quantity"].fillna(1)
    cleaned["region"] = cleaned["region"].fillna("Unknown")
    cleaned["product"] = cleaned["product"].fillna("Unknown Product")
    cleaned["category"] = cleaned["category"].fillna("Uncategorized")

    cleaned = cleaned.dropna(subset=["order_date", "unit_price"])
    cleaned = cleaned[(cleaned["quantity"] > 0) & (cleaned["unit_price"] > 0)]

    cleaned["revenue"] = cleaned["quantity"] * cleaned["unit_price"]
    cleaned["order_month"] = cleaned["order_date"].dt.to_period("M").astype(str)

    return cleaned.reset_index(drop=True)


def create_summary_tables(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Create summary tables used for reporting."""
    monthly_revenue = (
        df.groupby("order_month", as_index=False)["revenue"]
        .sum()
        .sort_values("order_month")
    )

    product_revenue = (
        df.groupby("product", as_index=False)["revenue"]
        .sum()
        .sort_values("revenue", ascending=False)
    )

    region_revenue = (
        df.groupby("region", as_index=False)["revenue"]
        .sum()
        .sort_values("revenue", ascending=False)
    )

    category_revenue = (
        df.groupby("category", as_index=False)["revenue"]
        .sum()
        .sort_values("revenue", ascending=False)
    )

    return {
        "monthly_revenue": monthly_revenue,
        "product_revenue": product_revenue,
        "region_revenue": region_revenue,
        "category_revenue": category_revenue,
    }
