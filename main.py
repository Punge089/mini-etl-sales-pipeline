"""Main script for the Mini ETL Sales Pipeline project."""

import logging
from pathlib import Path

from src.extract import load_sales_data
from src.transform import clean_sales_data, create_summary_tables
from src.load import save_cleaned_csv, load_to_sqlite
from src.queries import get_business_metrics
from src.report import save_bar_chart, write_data_quality_report, write_markdown_report


RAW_DATA_PATH = Path("data/raw/sales.csv")
CLEANED_DATA_PATH = Path("data/processed/cleaned_sales.csv")
DATABASE_PATH = Path("database/sales_pipeline.db")
REPORT_PATH = Path("output/reports/sales_summary.md")
QUALITY_REPORT_PATH = Path("output/reports/data_quality_report.md")
MONTHLY_CHART_PATH = Path("output/charts/monthly_revenue.png")
PRODUCT_CHART_PATH = Path("output/charts/top_products.png")
LOG_PATH = Path("output/logs/pipeline.log")


def setup_logging() -> None:
    """Configure console and file logging for the pipeline run."""
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(LOG_PATH, mode="w", encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )
    logging.getLogger("matplotlib").setLevel(logging.WARNING)


def main() -> None:
    """Run the full ETL pipeline."""
    setup_logging()
    logger = logging.getLogger(__name__)

    logger.info("Starting Mini ETL Sales Pipeline...")

    raw_df = load_sales_data(RAW_DATA_PATH)
    logger.info("Extracted %s raw rows.", len(raw_df))

    cleaned_df, quality_stats = clean_sales_data(raw_df)
    logger.info(
        "Removed %s rows and transformed %s rows.",
        quality_stats["rows_removed_total"],
        quality_stats["rows_transformed"],
    )

    save_cleaned_csv(cleaned_df, CLEANED_DATA_PATH)
    load_to_sqlite(cleaned_df, DATABASE_PATH)
    logger.info("Loaded %s rows into CSV and SQLite.", quality_stats["final_rows_loaded"])

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
    write_data_quality_report(quality_stats, QUALITY_REPORT_PATH)

    logger.info("Generated charts and Markdown reports.")
    logger.info("Cleaned data: %s", CLEANED_DATA_PATH)
    logger.info("Database: %s", DATABASE_PATH)
    logger.info("Sales report: %s", REPORT_PATH)
    logger.info("Data quality report: %s", QUALITY_REPORT_PATH)
    logger.info("Log file: %s", LOG_PATH)
    logger.info("Pipeline completed successfully.")


if __name__ == "__main__":
    main()
