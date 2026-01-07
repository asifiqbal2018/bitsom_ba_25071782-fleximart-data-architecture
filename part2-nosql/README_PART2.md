# FlexiMart – Part 2: NoSQL (MongoDB)

## What this part does
- Justifies why MongoDB fits a flexible product catalog use case
- Performs basic MongoDB operations (import, query, aggregation, update)

## Files
- `nosql_analysis.md` — theory report (RDBMS limits, MongoDB benefits, trade-offs)
- `mongodb_operations.js` — 5 MongoDB operations
- `products_catalog.json` — sample product catalog JSON

## Import JSON to MongoDB
### Option A: Using mongosh script (works even without mongoimport)
From `part2-nosql/`:
```powershell
mongosh "mongodb://localhost:27017/fleximart" mongodb_operations.js
```