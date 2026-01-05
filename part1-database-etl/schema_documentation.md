# Flexi Mart – Database Schema Documentation

## 1) Entity–Relationship Description 

### ENTITY: customers
**Purpose:** Stores customer profile and contact information.

**Attributes:**
- **customer_id (PK):** Unique identifier for each customer (auto-generated surrogate key).
- **first_name:** Customer’s first name.
- **last_name:** Customer’s last name.
- **email (UNIQUE, NOT NULL):** Customer’s email address (must be unique to avoid duplicate accounts).
- **phone (NULL):** Customer’s phone number (stored in standardized format when available).
- **city (NULL):** Customer’s city of residence.
- **registration_date (NULL):** Date the customer registered.

---

### ENTITY: products
**Purpose:** Stores product master information for items sold by Flexi Mart.

**Attributes:**
- **product_id (PK):** Unique identifier for each product (auto-generated surrogate key).
- **product_name (NOT NULL):** Name of the product.
- **category (NOT NULL):** Product category (standardized casing like “Electronics”, “Fashion”).
- **price (NOT NULL):** Unit price of the product.
- **stock_quantity (DEFAULT 0):** Current stock available for the product.

---

### ENTITY: orders
**Purpose:** Stores order-level information (who ordered, when, total, and status).

**Attributes:**
- **order_id (PK):** Unique identifier for each order (auto-generated surrogate key).
- **customer_id (FK → customers.customer_id, NOT NULL):** Customer who placed the order.
- **order_date (NOT NULL):** Date the order was placed.
- **total_amount (NOT NULL):** Total amount for the order (sum of all item subtotals).
- **status (DEFAULT 'Pending'):** Order status such as Pending/Completed/Cancelled.

---

### ENTITY: order_items
**Purpose:** Stores product-level line items inside each order.

**Attributes:**
- **order_item_id (PK):** Unique identifier for each order item record (auto-generated surrogate key).
- **order_id (FK → orders.order_id, NOT NULL):** Order to which this line item belongs.
- **product_id (FK → products.product_id, NOT NULL):** Product being purchased.
- **quantity (NOT NULL):** Number of units purchased for this product.
- **unit_price (NOT NULL):** Price per unit at the time of purchase.
- **subtotal (NOT NULL):** quantity × unit_price.

---

## 2) Relationships
- **customers → orders (1 : M)**  
  One customer can place **many** orders, but each order belongs to **one** customer.

- **orders → order_items (1 : M)**  
  One order can contain **many** line items, but each line item belongs to **one** order.

- **products → order_items (1 : M)**  
  One product can appear in **many** order items, but each order item references **one** product.

This design also forms an **M : N relationship between orders and products**, resolved using the `order_items` junction table.

---

## 3) Normalization Explanation (3NF)

This database design is in **Third Normal Form (3NF)** because every non-key attribute depends only on the key, the whole key, and nothing but the key.  
For the **customers** table, the primary key is `customer_id`, and all attributes such as `first_name`, `last_name`, `email`, `phone`, `city`, and `registration_date` describe only that customer. A key functional dependency is:  
`customer_id → first_name, last_name, email, phone, city, registration_date`.  
For **products**, the dependency is:  
`product_id → product_name, category, price, stock_quantity`.  
For **orders**, we have:  
`order_id → customer_id, order_date, total_amount, status`.  
For **order_items**, the dependency is:  
`order_item_id → order_id, product_id, quantity, unit_price, subtotal`.

The schema avoids **update anomalies** because product and customer details are stored once (not repeated in multiple orders). It avoids **insert anomalies** because you can add a new customer or product without requiring an order to exist. It avoids **delete anomalies** because deleting an order does not delete the product or customer master records (they remain stored in their respective tables). Using a separate `order_items` table prevents repeating product attributes in the order table and cleanly represents the many-to-many relationship between orders and products.

---

## 4) Sample Data Representation (Example Records)

### customers (sample)
| customer_id | first_name | last_name | email              | phone           | city     | registration_date |
|------------:|-----------|----------|-------------------|----------------|----------|------------------|
| 1           | Asha      | Khan     | asha@gmail.com     | +91-9876543210 | Mumbai   | 2025-01-10       |
| 2           | Ravi      | Kumar    | ravi@gmail.com     | +91-9123456789 | Delhi    | 2025-02-05       |
| 3           | Neha      | Singh    | neha@gmail.com     |                | Bengaluru| 2025-03-12       |

### products (sample)
| product_id | product_name        | category     | price    | stock_quantity |
|----------:|---------------------|--------------|---------:|---------------:|
| 1         | Samsung Galaxy S21  | Electronics  | 45999.00 | 150            |
| 2         | Nike Running Shoes  | Fashion      | 3499.00  | 80             |
| 3         | Organic Almonds     | Groceries    | 899.00   | 0              |

### orders (sample)
| order_id | customer_id | order_date  | total_amount | status    |
|--------:|------------:|------------|-------------:|----------|
| 1       | 1           | 2025-05-10 | 49498.00     | Pending  |
| 2       | 2           | 2025-05-11 | 3499.00      | Completed|

### order_items (sample)
| order_item_id | order_id | product_id | quantity | unit_price | subtotal  |
|-------------:|---------:|-----------:|---------:|-----------:|----------:|
| 1            | 1        | 1          | 1        | 45999.00   | 45999.00  |
| 2            | 1        | 3          | 4        | 899.00     | 3596.00   |
| 3            | 2        | 2          | 1        | 3499.00    | 3499.00   |
