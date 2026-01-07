# FlexiMart – Part 1: Database ETL

## What this part does
Builds an ETL pipeline that:
- Reads raw CSV files from `data/raw/`
- Cleans data (duplicates, missing values, standardization)
- Loads into PostgreSQL tables: `customers`, `products`, `orders`, `order_items`
- Generates a data quality report

## Files
- `etl_pipeline.py` — main ETL script
- `schema_documentation.md` — schema + ER description + 3NF notes + sample rows
- `business_queries.sql` — business SQL queries (3 scenarios)
- `data_quality_report.txt` — generated ETL quality report
- `requirements.txt` — Python dependencies

## Setup
1. Create & activate virtual environment (from project root):
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
2. Install dependencies:
    ```powershell
    python -m pip install -r part1-database-etl/requirements.txt
    ```

3. Configure .env (at project root):
    ```powershell
    DB_URL=postgresql+psycopg2://postgres:<PASSWORD>@localhost:5432/fleximart
    RAW_DIR=./data/raw
    REPORT_PATH=./part1-database-etl/data_quality_report.txt
    LOG_PATH=./etl.log
    ```powershell
