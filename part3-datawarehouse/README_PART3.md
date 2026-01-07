# FlexiMart – Part 3: Data Warehouse (Star Schema)

## What this part does
- Builds a star schema in `fleximart_dw`
- Loads warehouse data
- Runs analytics queries for reporting insights

## Files
- `star_schema_design.md` — star schema explanation (grain, facts, dimensions)
- `warehouse_schema.sql` — create DW tables
- `warehouse_data.sql` — load sample warehouse data
- `analytics_queries.sql` — analytical SQL queries

## Setup (PostgreSQL)
1. Create database:
```sql
CREATE DATABASE fleximart_dw;
```
2. Run schema + load data:
```powershell
psql -U postgres -d fleximart_dw -f part3-datawarehouse/warehouse_schema.sql
psql -U postgres -d fleximart_dw -f part3-datawarehouse/warehouse_data.sql
```
3. Run analytics queries:
```powershell
psql -U postgres -d fleximart_dw -f part3-datawarehouse/analytics_queries.sql
```
