-- analytics_queries.sql
-- Task 3.3: OLAP Analytics Queries

-- =========================================================
-- Query 1: Monthly Sales Drill-Down Analysis
-- Business Scenario: "The CEO wants to see sales performance broken down by time periods.
-- Start with yearly total, then quarterly, then monthly sales for 2024."
-- Demonstrates: Drill-down from Year → Quarter → Month
-- =========================================================
SELECT
    d.year,
    d.quarter,
    d.month_name,
    SUM(f.total_amount)    AS total_sales,
    SUM(f.quantity_sold)   AS total_quantity
FROM fact_sales f
JOIN dim_date d
  ON f.date_key = d.date_key
WHERE d.year = 2024
GROUP BY
    d.year,
    d.quarter,
    d.month,
    d.month_name
ORDER BY
    d.year,
    d.quarter,
    d.month;

-- =========================================================
-- Query 2: Product Performance Analysis (Top 10 Products)
-- Business Scenario: "The product manager needs to identify top-performing products.
-- Show the top 10 products by revenue, along with their category, total units sold,
-- and revenue contribution percentage."
-- Includes: Revenue percentage calculation using window function
-- =========================================================
SELECT
    p.product_name,
    p.category,
    SUM(f.quantity_sold) AS units_sold,
    SUM(f.total_amount)  AS revenue,
    ROUND(
        (SUM(f.total_amount) / NULLIF(SUM(SUM(f.total_amount)) OVER (), 0)) * 100,
        2
    ) AS revenue_percentage
FROM fact_sales f
JOIN dim_product p
  ON f.product_key = p.product_key
GROUP BY
    p.product_name,
    p.category
ORDER BY
    revenue DESC
LIMIT 10;

-- =========================================================
-- Query 3: Customer Segmentation Analysis
-- Business Scenario: "Marketing wants to target high-value customers.
-- Segment customers into 'High Value' (>₹50,000 spent),
-- 'Medium Value' (₹20,000-₹50,000), and 'Low Value' (<₹20,000).
-- Show count of customers and total revenue in each segment."
-- Segments: High/Medium/Low value customers
-- =========================================================
WITH customer_spend AS (
    SELECT
        c.customer_key,
        c.customer_name,
        SUM(f.total_amount) AS total_spent
    FROM fact_sales f
    JOIN dim_customer c
      ON f.customer_key = c.customer_key
    GROUP BY
        c.customer_key,
        c.customer_name
),
segmented AS (
    SELECT
        customer_key,
        customer_name,
        total_spent,
        CASE
            WHEN total_spent > 50000 THEN 'High Value'
            WHEN total_spent BETWEEN 20000 AND 50000 THEN 'Medium Value'
            ELSE 'Low Value'
        END AS customer_segment
    FROM customer_spend
)
SELECT
    customer_segment,
    COUNT(*)              AS customer_count,
    SUM(total_spent)      AS total_revenue,
    ROUND(AVG(total_spent), 2) AS avg_revenue_per_customer
FROM segmented
GROUP BY
    customer_segment
ORDER BY
    CASE customer_segment
        WHEN 'High Value' THEN 1
        WHEN 'Medium Value' THEN 2
        ELSE 3
    END;
