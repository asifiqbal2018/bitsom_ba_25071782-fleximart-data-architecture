# FlexiMart Data Architecture Project

**Student Name:** Mohammed Asif Iqbal
**Student ID:** [Your ID]
**Email:** asifiqbal149@gmail.com
**Date:** 1/5/2026

## Project Overview

This project builds an end-to-end data engineering workflow for **FlexiMart** across three parts: (1) a relational database ETL pipeline to load and clean transactional data, (2) NoSQL analysis and operations using MongoDB for flexible product/catalog queries, and (3) a dimensional **data warehouse (star schema)** to support OLAP-style analytics. The final deliverable includes schema design, realistic warehouse seed data, and analytical SQL queries for business reporting.

## Repository Structure
├── part1-database-etl/
│   ├── etl_pipeline.py
│   ├── schema_documentation.md
│   ├── business_queries.sql
│   └── data_quality_report.txt
├── part2-nosql/
│   ├── nosql_analysis.md
│   ├── mongodb_operations.js
│   └── products_catalog.json
├── part3-datawarehouse/
│   ├── star_schema_design.md
│   ├── warehouse_schema.sql
│   ├── warehouse_data.sql
│   └── analytics_queries.sql
└── README.md

## Technologies Used

- Python 3.x, pandas, mysql-connector-python
- MySQL 8.0 / PostgreSQL 14
- MongoDB 6.0

## Setup Instructions

### Database Setup

```bash
# Create databases
createdb fleximart;
createdb fleximart_dw;

# Run Part 1 - ETL Pipeline
python part1-database-etl/etl_pipeline.py

# Run Part 1 - Business Queries
psql -d fleximart -f part1-database-etl/business_queries.sql

# Run Part 3 - Data Warehouse (PostgreSQL)
psql -d fleximart_dw -f part3-datawarehouse/warehouse_schema.sql
psql -d fleximart_dw -f part3-datawarehouse/warehouse_data.sql
psql -d fleximart_dw -f part3-datawarehouse/analytics_queries.sql

### MongoDB Setup

# Option 1: Run JS file in mongosh
mongosh "mongodb://localhost:27017/fleximart" --file part2-nosql/mongodb_operations.js

# Option 2: If mongodb_operations.js expects to import JSON itself, just run it
mongosh --file part2-nosql/mongodb_operations.js


## Key Learnings
- Built an ETL pipeline to clean and load data into a relational database and validated results with business queries.
- Learned how NoSQL (MongoDB) supports flexible document-based exploration and fast iteration for semi-structured data.
- Designed a star schema with proper grain, facts, and dimensions to support analytics use cases.
- Used SQL aggregation, joins, and OLAP concepts to generate insights like drill-down reporting, top products, and customer segmentation.

## Challenges Faced
1. **Inconsistent source data during ETL (nulls, types, formatting issues)**  
   **Solution:** Implemented cleaning rules (type casting, null handling, standardized formats) and verified outputs using row count checks and query validations.

2. **Avoiding foreign key violations while loading the warehouse**  
   **Solution:** Loaded dimensions first, used consistent surrogate key lookups for facts, and ran validation queries to confirm referential integrity and correct total calculations.
