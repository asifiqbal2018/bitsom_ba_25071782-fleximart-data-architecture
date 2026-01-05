# Star Schema Design Documentation

## Section 1: Schema Overview

### FACT TABLE: `fact_sales`
**Grain:** One row per product per order line item  
**Business Process:** Sales transactions

**Measures (Numeric Facts):**
- **quantity_sold:** Number of units sold
- **unit_price:** Price per unit at time of sale
- **discount_amount:** Discount applied
- **total_amount:** Final amount  
  `total_amount = (quantity_sold × unit_price) - discount_amount`

**Foreign Keys:**
- **date_key** → `dim_date`
- **product_key** → `dim_product`
- **customer_key** → `dim_customer`

---

### DIMENSION TABLE: `dim_date`
**Purpose:** Date dimension for time-based analysis  
**Type:** Conformed dimension

**Attributes:**
- **date_key (PK):** Surrogate key (integer, format: YYYYMMDD)
- **full_date:** Actual date
- **day_of_week:** Monday, Tuesday, etc.
- **month:** 1–12
- **month_name:** January, February, etc.
- **quarter:** Q1, Q2, Q3, Q4
- **year:** 2023, 2024, etc.
- **is_weekend:** Boolean

---

### DIMENSION TABLE: `dim_product`
**Purpose:** Product dimension for product/category/brand analysis  
**Type:** Slowly Changing Dimension (SCD) (Type 1 or Type 2 based on business requirement)

**Attributes:**
- **product_key (PK):** Surrogate key (integer)
- **product_id (NK):** Natural/business key from source system
- **product_name:** Name of the product (e.g., Laptop)
- **brand:** Brand name
- **category:** Category (e.g., Electronics)
- **sub_category:** Subcategory (e.g., Computers)
- **sku:** Stock keeping unit code
- **is_active:** Boolean flag to indicate active/inactive product

---

### DIMENSION TABLE: `dim_customer`
**Purpose:** Customer dimension for customer/location/segment analysis  
**Type:** Slowly Changing Dimension (SCD) (Type 1 or Type 2 based on business requirement)

**Attributes:**
- **customer_key (PK):** Surrogate key (integer)
- **customer_id (NK):** Natural/business key from source system
- **customer_name:** Full customer name
- **gender:** Customer gender (if available)
- **email:** Email address
- **phone:** Phone number
- **city:** City (e.g., Mumbai)
- **state:** State/Region
- **country:** Country
- **customer_segment:** Segment label (e.g., Retail, Premium)
- **is_active:** Boolean flag to indicate active/inactive customer

---

## Section 2: Design Decisions (150 words)

This star schema uses transaction line-item granularity because it captures the most detailed level of sales activity: each product in each order is stored as a separate row. This enables accurate analysis of product performance, discounts, and revenue at the item level, while still allowing higher-level aggregations like daily totals, monthly trends, and category-level sales. Surrogate keys are used instead of natural keys to improve join performance (integer keys), ensure stable relationships even if source system IDs change, and support slowly changing dimensions where customer or product attributes may evolve over time. Natural keys are still stored in the dimension tables for traceability back to the source. This design supports drill-down and roll-up operations by allowing analysts to roll up measures across hierarchies such as date → month → quarter → year, product → category → subcategory, and customer → city → state → country, and drill down to individual transactions when required.

---

## Section 3: Sample Data Flow

### Source Transaction
Order #101, Customer "John Doe", Product "Laptop", Qty: 2, Price: 50000, Discount: 0  
Transaction Date: 2024-01-15

### Becomes in Data Warehouse

**fact_sales:**
```json
{
  "date_key": 20240115,
  "product_key": 5,
  "customer_key": 12,
  "quantity_sold": 2,
  "unit_price": 50000,
  "discount_amount": 0,
  "total_amount": 100000
}
```
 **dim_date:**
 ```json
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
```
**dim_product**
```json
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
```
**dim_customer**
```json
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
```
