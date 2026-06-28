# Project Explanation for Interview

Use this to explain the project if someone asks.

## 1. What does this project do?

This project is a mini ETL sales data pipeline. It takes raw sales data from a CSV file, cleans and transforms the data, loads it into a SQLite database, and generates reports and charts.

## 2. Why is it related to Data Engineering?

Data Engineering is about preparing reliable data for analytics or downstream systems. This project demonstrates a simple version of that workflow:
- Extract data from a raw source
- Clean and transform the data
- Load data into a database
- Query the database using SQL
- Generate useful reports

## 3. What does each file do?

- `main.py`: Runs the full pipeline
- `extract.py`: Reads raw CSV data
- `transform.py`: Cleans the data and creates summary tables
- `load.py`: Saves cleaned data into CSV and SQLite
- `queries.py`: Runs SQL queries
- `report.py`: Generates charts and Markdown reports

## 4. What cleaning steps are used?

- Remove duplicate rows
- Convert invalid dates into missing values
- Convert quantity and unit price into numbers
- Fill missing quantity with 1
- Fill missing region with `Unknown`
- Remove rows with invalid dates or missing price
- Calculate revenue using `quantity * unit_price`

## 5. What SQL queries are included?

- Total revenue
- Monthly revenue
- Top 5 products by revenue
- Revenue by region
- Average order value

## 6. What could be improved later?

- Add automated tests
- Add larger datasets
- Use DuckDB or PostgreSQL instead of SQLite
- Schedule the pipeline with Airflow
- Add dashboard using Streamlit
- Add data validation rules
