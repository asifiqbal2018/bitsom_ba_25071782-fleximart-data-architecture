Star Schema Design Documentation
Section 1: Schema Overview
FACT TABLE: fact_sales

Grain: One row per product per order line item (i.e., each item in an order becomes one fact row).
Business Process: Sales transactions (customer purchases).

Measures (Numeric Facts):

quantity_sold: Number of units sold for the line item

unit_price: Price per unit at the time of sale

discount_amount: Discount applied on that line item

total_amount: Final line total
total_amount = (quantity_sold × unit_price) - discount_amount

Foreign Keys:

date_key → dim_date

product_key → dim_product

customer_key → dim_customer

DIMENSION TABLE: dim_date

Purpose: Date dimension for time-based analysis (daily, monthly, quarterly, yearly trends).
Type: Conformed dimension (usable across multiple fact tables if needed).

Attributes:

date_key (PK): Surrogate key (integer, format: YYYYMMDD)

full_date: Actual date (DATE)

day_of_week: Monday, Tuesday, etc.

month: 1–12

month_name: January, February, etc.

quarter: Q1, Q2, Q3, Q4

year: 2023, 2024, etc.

is_weekend: Boolean (true/false)

DIMENSION TABLE: dim_product

Purpose: Stores descriptive product details for product/category-based analysis.
Type: Slowly changing dimension (commonly SCD Type 2 or Type 1 depending on need; supports consistent history if implemented).

Attributes:

product_key (PK): Surrogate key (integer)

product_id (NK): Natural/business key from source system (string/int)

product_name: Product name (e.g., Laptop)

brand: Brand name (e.g., Dell, HP)

category: High-level category (e.g., Electronics)

sub_category: Subcategory (e.g., Computers)

sku: Stock keeping unit code

is_active: Boolean flag for active/inactive product

DIMENSION TABLE: dim_customer

Purpose: Stores customer details for customer segmentation and location-based analytics.
Type: Slowly changing dimension (supports tracking changes like city/address over time if implemented).

Attributes:

customer_key (PK): Surrogate key (integer)

customer_id (NK): Natural/business key from source system (string/int)

customer_name: Full customer name

gender: Customer gender (if available)

email: Email address

phone: Phone number

city: City (e.g., Mumbai)

state: State/Region

country: Country

customer_segment: Segment label (e.g., Retail, Corporate, Premium)

is_active: Boolean flag for active/inactive customer

Section 2: Design Decisions (≈150 words)

This schema uses transaction line-item granularity because it preserves the most detailed level of sales data: each product in each order is captured separately. This enables accurate reporting for item-level metrics like product performance, basket analysis, and detailed revenue calculations. Aggregations (daily/monthly totals, category totals, customer totals) can be derived reliably from the atomic facts, which is essential for flexible analytics.

Surrogate keys are used instead of natural keys to improve performance (integer joins are faster), isolate the warehouse from changes in operational IDs, and support slowly changing dimensions where customer/product attributes may change over time. Natural keys are still stored in dimensions for traceability, but surrogate keys ensure stable relationships between facts and dimensions.

This design supports drill-down and roll-up because users can roll up measures (total sales, quantity) across dimension hierarchies (date → month → quarter → year; product → category; customer → city/state/country) and drill down back to individual transactions when needed.

Section 3: Sample Data Flow
Source Transaction

Order #101, Customer "John Doe", Product "Laptop", Qty 2, Price 50000, Discount 0
Transaction Date: 2024-01-15

Becomes in Data Warehouse

fact_sales:

{
  "date_key": 20240115,
  "product_key": 5,
  "customer_key": 12,
  "quantity_sold": 2,
  "unit_price": 50000,
  "discount_amount": 0,
  "total_amount": 100000
}


dim_date:

{
  "date_key": 20240115,
  "full_date": "2024-01-15",
  "day_of_week": "Monday",
  "month": 1,
  "month_name": "January",
  "quarter": "Q1",
  "year": 2024,
  "is_weekend": false
}


dim_product:

{
  "product_key": 5,
  "product_id": "P1005",
  "product_name": "Laptop",
  "brand": "Generic",
  "category": "Electronics",
  "sub_category": "Computers",
  "sku": "LAP-001",
  "is_active": true
}


dim_customer:

{
  "customer_key": 12,
  "customer_id": "C1012",
  "customer_name": "John Doe",
  "email": "john.doe@email.com",
  "phone": "9999999999",
  "city": "Mumbai",
  "state": "Maharashtra",
  "country": "India",
  "customer_segment": "Retail",
  "is_active": true
}