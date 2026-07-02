"""Transform module for cleaning and preparing sales data."""

import logging

import pandas as pd


logger = logging.getLogger(__name__)


REQUIRED_COLUMNS = [
    "order_id",
    "order_date",
    "customer_id",
    "product",
    "category",
    "quantity",
    "unit_price",
    "region",
]


def clean_sales_data(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
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
        A cleaned sales DataFrame and a small data quality summary.
    """
    cleaned = df.copy()
    cleaned.columns = [col.strip().lower() for col in cleaned.columns]

    missing_columns = [col for col in REQUIRED_COLUMNS if col not in cleaned.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")

    stats = {
        "raw_rows": int(len(cleaned)),
        "raw_columns": int(len(cleaned.columns)),
    }

    duplicate_count = int(cleaned.duplicated().sum())
    cleaned = cleaned.drop_duplicates()
    stats["duplicate_rows_removed"] = duplicate_count
    stats["rows_after_duplicates"] = int(len(cleaned))

    text_columns = ["customer_id", "product", "category", "region"]
    for column in text_columns:
        cleaned[column] = cleaned[column].astype("string").str.strip()
        cleaned[column] = cleaned[column].replace("", pd.NA)

    missing_text_values = {
        column: int(cleaned[column].isna().sum()) for column in text_columns
    }

    order_dates = pd.to_datetime(cleaned["order_date"], errors="coerce")
    quantities = pd.to_numeric(cleaned["quantity"], errors="coerce")
    unit_prices = pd.to_numeric(cleaned["unit_price"], errors="coerce")

    original_quantity_missing = cleaned["quantity"].isna()
    stats["invalid_or_missing_dates_removed"] = int(order_dates.isna().sum())
    stats["missing_quantity_filled"] = int(original_quantity_missing.sum())
    stats["invalid_quantity_removed"] = int(
        (quantities.isna() & ~original_quantity_missing).sum()
    )
    stats["missing_or_invalid_unit_price_removed"] = int(unit_prices.isna().sum())

    cleaned["order_date"] = order_dates
    cleaned["quantity"] = quantities
    cleaned["unit_price"] = unit_prices

    cleaned.loc[original_quantity_missing, "quantity"] = 1
    cleaned["region"] = cleaned["region"].fillna("Unknown")
    cleaned["product"] = cleaned["product"].fillna("Unknown Product")
    cleaned["category"] = cleaned["category"].fillna("Uncategorized")
    cleaned["customer_id"] = cleaned["customer_id"].fillna("Unknown Customer")

    stats["missing_text_values_filled"] = missing_text_values
    stats["text_values_filled_total"] = int(sum(missing_text_values.values()))

    stats["non_positive_quantity_removed"] = int((cleaned["quantity"] <= 0).sum())
    stats["non_positive_unit_price_removed"] = int((cleaned["unit_price"] <= 0).sum())

    invalid_rows = (
        cleaned["order_date"].isna()
        | cleaned["quantity"].isna()
        | cleaned["unit_price"].isna()
        | (cleaned["quantity"] <= 0)
        | (cleaned["unit_price"] <= 0)
    )

    cleaned = cleaned.loc[~invalid_rows].copy()

    cleaned["revenue"] = cleaned["quantity"] * cleaned["unit_price"]
    cleaned["order_month"] = cleaned["order_date"].dt.to_period("M").astype(str)

    stats["invalid_rows_removed_after_deduplication"] = int(invalid_rows.sum())
    stats["final_rows_loaded"] = int(len(cleaned))
    stats["rows_removed_total"] = int(stats["raw_rows"] - stats["final_rows_loaded"])
    stats["rows_transformed"] = int(len(cleaned))
    stats["new_columns_created"] = ["revenue", "order_month"]

    logger.info(
        "Cleaned %s raw rows into %s final rows.",
        stats["raw_rows"],
        stats["final_rows_loaded"],
    )

    return cleaned.reset_index(drop=True), stats


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
