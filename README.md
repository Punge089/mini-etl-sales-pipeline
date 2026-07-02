# Mini ETL Sales Pipeline

This is a beginner-friendly Data Engineering portfolio project. It shows a small ETL pipeline that reads messy sales data from a CSV file, cleans it with Python and Pandas, loads it into SQLite, and creates a few simple reports and charts.

I kept the project small on purpose so the main ETL idea is easy to follow.

## Project Overview

The sample dataset contains sales transactions with some common data quality problems:

- duplicate rows
- missing product, region, quantity, and unit price values
- invalid dates
- invalid or missing numeric values

The pipeline handles those issues and records what happened during the run.

## ETL Workflow

1. **Extract**
   - Read raw sales data from `data/raw/sales.csv`

2. **Transform**
   - Standardize column names
   - Remove duplicate rows
   - Convert order dates, quantities, and prices to the correct data types
   - Fill simple missing values where it makes sense
   - Remove rows with invalid dates or prices
   - Create `revenue` and `order_month` columns

3. **Load**
   - Save cleaned data to `data/processed/cleaned_sales.csv`
   - Load cleaned data into `database/sales_pipeline.db`

4. **Report**
   - Run SQL queries for business metrics
   - Generate Markdown reports
   - Generate revenue charts
   - Save a pipeline log file

## Project Structure

```text
mini-etl-sales-pipeline/
├── data/
│   ├── raw/
│   │   └── sales.csv
│   └── processed/
│       └── cleaned_sales.csv
├── database/
│   └── sales_pipeline.db
├── output/
│   ├── charts/
│   │   ├── monthly_revenue.png
│   │   └── top_products.png
│   ├── logs/
│   │   └── pipeline.log
│   └── reports/
│       ├── data_quality_report.md
│       └── sales_summary.md
├── src/
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   ├── queries.py
│   └── report.py
├── main.py
├── requirements.txt
└── README.md
```

## How to Run

Create and activate a virtual environment:

```bash
python -m venv venv
```

On Windows:

```bash
.\venv\Scripts\activate
```

On macOS or Linux:

```bash
source venv/bin/activate
```

Install the Python packages:

```bash
pip install -r requirements.txt
```

Run the ETL pipeline:

```bash
python main.py
```

## Outputs

After running the project, these files are created or updated:

- `data/processed/cleaned_sales.csv` - cleaned sales dataset
- `database/sales_pipeline.db` - SQLite database with a `sales` table
- `output/reports/sales_summary.md` - SQL-based sales summary report
- `output/reports/data_quality_report.md` - data validation and cleaning summary
- `output/charts/monthly_revenue.png` - monthly revenue chart
- `output/charts/top_products.png` - top products chart
- `output/logs/pipeline.log` - log file for the pipeline run

## Data Quality Checks

The transform step tracks:

- how many raw rows were extracted
- how many duplicate rows were removed
- how many rows were removed because of invalid dates or numeric values
- how many missing values were filled
- how many final rows were loaded
- how many rows were transformed with new calculated columns

The results are saved in `output/reports/data_quality_report.md`.

## Skills Practiced

- Reading CSV files with Pandas
- Cleaning and validating messy data
- Tracking basic data quality metrics
- Loading data into SQLite
- Writing SQL queries for simple analytics
- Creating charts with Matplotlib
- Organizing a small Python data project
- Using logging to make the pipeline easier to debug

## What I Learned

This project helped me understand that an ETL pipeline is not only about moving data from one place to another. The cleaning and validation steps are important because bad dates, missing prices, and duplicates can change the final business results.

I also practiced separating the project into small files, so each part of the pipeline has its own job: extract, transform, load, query, and report.
