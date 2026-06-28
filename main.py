"""Main script for the Mini ETL Sales Pipeline project."""

from pathlib import Path

from src.extract import load_sales_data
from src.transform import clean_sales_data, create_summary_tables
from src.load import save_cleaned_csv, load_to_sqlite
from src.queries import get_business_metrics
from src.report import save_bar_chart, write_markdown_report


RAW_DATA_PATH = Path("data/raw/sales.csv")
CLEANED_DATA_PATH = Path("data/processed/cleaned_sales.csv")
DATABASE_PATH = Path("database/sales_pipeline.db")
REPORT_PATH = Path("output/reports/sales_summary.md")
MONTHLY_CHART_PATH = Path("output/charts/monthly_revenue.png")
PRODUCT_CHART_PATH = Path("output/charts/top_products.png")


def main() -> None:
    """Run the full ETL pipeline."""
    print("Starting Mini ETL Sales Pipeline...")

    raw_df = load_sales_data(RAW_DATA_PATH)
    print(f"Extracted {len(raw_df)} raw rows.")

    cleaned_df = clean_sales_data(raw_df)
    print(f"Transformed into {len(cleaned_df)} cleaned rows.")

    save_cleaned_csv(cleaned_df, CLEANED_DATA_PATH)
    load_to_sqlite(cleaned_df, DATABASE_PATH)
    print("Loaded cleaned data into CSV and SQLite database.")

    summary_tables = create_summary_tables(cleaned_df)
    sql_metrics = get_business_metrics(DATABASE_PATH)

    save_bar_chart(
        summary_tables["monthly_revenue"],
        "order_month",
        "revenue",
        "Monthly Revenue",
        MONTHLY_CHART_PATH,
    )

    save_bar_chart(
        summary_tables["product_revenue"].head(5),
        "product",
        "revenue",
        "Top 5 Products by Revenue",
        PRODUCT_CHART_PATH,
    )

    write_markdown_report(sql_metrics, REPORT_PATH)

    print("Generated charts and Markdown report.")
    print(f"Cleaned data: {CLEANED_DATA_PATH}")
    print(f"Database: {DATABASE_PATH}")
    print(f"Report: {REPORT_PATH}")
    print("Pipeline completed successfully.")


if __name__ == "__main__":
    main()
