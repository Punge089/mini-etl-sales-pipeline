# Mini ETL Sales Pipeline

A simple project that demonstrates an end-to-end ETL workflow using Python, Pandas, SQL, and SQLite.

## Project Overview

This project simulates a small sales data pipeline:

1. **Extract** raw sales data from a CSV file
2. **Transform** the dataset by cleaning missing values, removing duplicates, fixing data types, and calculating revenue
3. **Load** the cleaned data into a local SQLite database
4. **Query** the database using SQL
5. **Report** sales insights through Markdown reports and charts

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
│   ├── reports/
│   │   └── sales_summary.md
│   └── charts/
│       ├── monthly_revenue.png
│       └── top_products.png
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

## Features

- Load raw CSV sales data
- Clean duplicate and invalid records
- Handle missing values
- Convert date and numeric columns
- Calculate revenue
- Store cleaned data in SQLite
- Run SQL queries for business metrics
- Generate charts and Markdown report

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/Punge089/mini-etl-sales-pipeline.git
cd mini-etl-sales-pipeline
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

On Windows:

```bash
.\venv\Scripts\activate
```

On macOS/Linux:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the pipeline

```bash
python main.py
```

## Expected Output

After running the project, the pipeline will generate:

- `data/processed/cleaned_sales.csv`
- `database/sales_pipeline.db`
- `output/reports/sales_summary.md`
- `output/charts/monthly_revenue.png`
- `output/charts/top_products.png`

## Skills Demonstrated

- Python programming
- Data cleaning
- ETL pipeline design
- SQL querying
- Database loading
- Data reporting
- Data visualization
- GitHub project organization

## Resume Summary

Built a Python ETL pipeline to extract, clean, transform, and load sales data into a local SQL database. Used Pandas and SQL to generate business reports, including monthly revenue and top product performance.
