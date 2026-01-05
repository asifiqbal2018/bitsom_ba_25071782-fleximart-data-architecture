-- warehouse_data.sql
-- Load dimensions first, then facts (to satisfy FK constraints)

-- 1) dim_date: 30 dates (Jan-Feb 2024)
INSERT INTO dim_date (
    date_key, full_date, day_of_week, day_of_month, month, month_name, quarter, year, is_weekend
) VALUES
(20240101, '2024-01-01', 'Monday', 1, 1, 'January', 'Q1', 2024, FALSE),
(20240102, '2024-01-02', 'Tuesday', 2, 1, 'January', 'Q1', 2024, FALSE),
(20240103, '2024-01-03', 'Wednesday', 3, 1, 'January', 'Q1', 2024, FALSE),
(20240104, '2024-01-04', 'Thursday', 4, 1, 'January', 'Q1', 2024, FALSE),
(20240105, '2024-01-05', 'Friday', 5, 1, 'January', 'Q1', 2024, FALSE),
(20240106, '2024-01-06', 'Saturday', 6, 1, 'January', 'Q1', 2024, TRUE),
(20240107, '2024-01-07', 'Sunday', 7, 1, 'January', 'Q1', 2024, TRUE),
(20240108, '2024-01-08', 'Monday', 8, 1, 'January', 'Q1', 2024, FALSE),
(20240109, '2024-01-09', 'Tuesday', 9, 1, 'January', 'Q1', 2024, FALSE),
(20240110, '2024-01-10', 'Wednesday', 10, 1, 'January', 'Q1', 2024, FALSE),
(20240111, '2024-01-11', 'Thursday', 11, 1, 'January', 'Q1', 2024, FALSE),
(20240112, '2024-01-12', 'Friday', 12, 1, 'January', 'Q1', 2024, FALSE),
(20240113, '2024-01-13', 'Saturday', 13, 1, 'January', 'Q1', 2024, TRUE),
(20240114, '2024-01-14', 'Sunday', 14, 1, 'January', 'Q1', 2024, TRUE),
(20240115, '2024-01-15', 'Monday', 15, 1, 'January', 'Q1', 2024, FALSE),
(20240201, '2024-02-01', 'Thursday', 1, 2, 'February', 'Q1', 2024, FALSE),
(20240202, '2024-02-02', 'Friday', 2, 2, 'February', 'Q1', 2024, FALSE),
(20240203, '2024-02-03', 'Saturday', 3, 2, 'February', 'Q1', 2024, TRUE),
(20240204, '2024-02-04', 'Sunday', 4, 2, 'February', 'Q1', 2024, TRUE),
(20240205, '2024-02-05', 'Monday', 5, 2, 'February', 'Q1', 2024, FALSE),
(20240206, '2024-02-06', 'Tuesday', 6, 2, 'February', 'Q1', 2024, FALSE),
(20240207, '2024-02-07', 'Wednesday', 7, 2, 'February', 'Q1', 2024, FALSE),
(20240208, '2024-02-08', 'Thursday', 8, 2, 'February', 'Q1', 2024, FALSE),
(20240209, '2024-02-09', 'Friday', 9, 2, 'February', 'Q1', 2024, FALSE),
(20240210, '2024-02-10', 'Saturday', 10, 2, 'February', 'Q1', 2024, TRUE),
(20240211, '2024-02-11', 'Sunday', 11, 2, 'February', 'Q1', 2024, TRUE),
(20240212, '2024-02-12', 'Monday', 12, 2, 'February', 'Q1', 2024, FALSE),
(20240213, '2024-02-13', 'Tuesday', 13, 2, 'February', 'Q1', 2024, FALSE),
(20240214, '2024-02-14', 'Wednesday', 14, 2, 'February', 'Q1', 2024, FALSE),
(20240215, '2024-02-15', 'Thursday', 15, 2, 'February', 'Q1', 2024, FALSE)
;

-- 2) dim_product: 15 products across 3 categories (Electronics, Home & Kitchen, Grocery)
-- Prices varied from ₹100 to ₹100,000
INSERT INTO dim_product (
    product_id, product_name, category, subcategory, unit_price
) VALUES
('P001', '4K OLED TV', 'Electronics', 'Television', 100000.00),
('P002', 'Gaming Laptop', 'Electronics', 'Computers', 99000.00),
('P003', 'Smartphone', 'Electronics', 'Mobiles', 45000.00),
('P004', 'Noise-Cancel Headphones', 'Electronics', 'Audio', 2500.00),
('P005', 'Bluetooth Speaker', 'Electronics', 'Audio', 3500.00),
('P006', 'Mixer Grinder', 'Home & Kitchen', 'Appliances', 4000.00),
('P007', 'Air Fryer', 'Home & Kitchen', 'Appliances', 8000.00),
('P008', 'Vacuum Cleaner', 'Home & Kitchen', 'Appliances', 12000.00),
('P009', 'Water Purifier', 'Home & Kitchen', 'Appliances', 18000.00),
('P010', 'Non-stick Pan', 'Home & Kitchen', 'Cookware', 1200.00),
('P011', 'Basmati Rice 5kg', 'Grocery', 'Staples', 900.00),
('P012', 'Olive Oil 1L', 'Grocery', 'Cooking', 650.00),
('P013', 'Protein Powder 1kg', 'Grocery', 'Health', 3200.00),
('P014', 'Coffee 500g', 'Grocery', 'Beverages', 450.00),
('P015', 'Dark Chocolate', 'Grocery', 'Snacks', 100.00)
;

-- 3) dim_customer: 12 customers across 4 cities
INSERT INTO dim_customer (
    customer_id, customer_name, city, state, customer_segment
) VALUES
('C001', 'John Doe', 'Mumbai', 'Maharashtra', 'Retail'),
('C002', 'Aisha Khan', 'Mumbai', 'Maharashtra', 'Premium'),
('C003', 'Rohit Sharma', 'Mumbai', 'Maharashtra', 'Retail'),
('C004', 'Neha Verma', 'Bengaluru', 'Karnataka', 'Retail'),
('C005', 'Arjun Reddy', 'Bengaluru', 'Karnataka', 'Corporate'),
('C006', 'Priya Nair', 'Bengaluru', 'Karnataka', 'Premium'),
('C007', 'Karan Singh', 'Delhi', 'Delhi', 'Retail'),
('C008', 'Meera Gupta', 'Delhi', 'Delhi', 'Premium'),
('C009', 'Vikram Malhotra', 'Delhi', 'Delhi', 'Corporate'),
('C010', 'Sara Ali', 'Hyderabad', 'Telangana', 'Retail'),
('C011', 'Imran Shaikh', 'Hyderabad', 'Telangana', 'Premium'),
('C012', 'Ananya Iyer', 'Hyderabad', 'Telangana', 'Corporate')
;

-- 4) fact_sales: 40 sales transactions
-- Realistic patterns:
-- - More transactions on weekends
-- - Higher quantities for grocery items
-- - Discounts occasionally applied
-- Note: product_key and customer_key are looked up via product_id/customer_id to avoid hardcoding identity values.
INSERT INTO fact_sales (
    date_key, product_key, customer_key, quantity_sold, unit_price, discount_amount, total_amount
) VALUES
(20240101, (SELECT product_key FROM dim_product WHERE product_id = 'P015'), (SELECT customer_key FROM dim_customer WHERE customer_id = 'C011'), 3, 100.00, 10.00, 290.00),
(20240102, (SELECT product_key FROM dim_product WHERE product_id = 'P011'), (SELECT customer_key FROM dim_customer WHERE customer_id = 'C004'), 1, 900.00, 50.00, 850.00),
(20240103, (SELECT product_key FROM dim_product WHERE product_id = 'P011'), (SELECT customer_key FROM dim_customer WHERE customer_id = 'C005'), 3, 900.00, 20.00, 2680.00),
(20240103, (SELECT product_key FROM dim_product WHERE product_id = 'P012'), (SELECT customer_key FROM dim_customer WHERE customer_id = 'C010'), 2, 650.00, 0.00, 1300.00),
(20240104, (SELECT product_key FROM dim_product WHERE product_id = 'P014'), (SELECT customer_key FROM dim_customer WHERE customer_id = 'C008'), 3, 450.00, 10.00, 1340.00),
(20240105, (SELECT product_key FROM dim_product WHERE product_id = 'P015'), (SELECT customer_key FROM dim_customer WHERE customer_id = 'C001'), 4, 100.00, 10.00, 390.00),
(20240105, (SELECT product_key FROM dim_product WHERE product_id = 'P010'), (SELECT customer_key FROM dim_customer WHERE customer_id = 'C006'), 2, 1200.00, 50.00, 2350.00),
(20240106, (SELECT product_key FROM dim_product WHERE product_id = 'P004'), (SELECT customer_key FROM dim_customer WHERE customer_id = 'C002'), 2, 2500.00, 100.00, 4900.00),
(20240106, (SELECT product_key FROM dim_product WHERE product_id = 'P006'), (SELECT customer_key FROM dim_customer WHERE customer_id = 'C009'), 3, 4000.00, 0.00, 12000.00),
(20240106, (SELECT product_key FROM dim_product WHERE product_id = 'P011'), (SELECT customer_key FROM dim_customer WHERE customer_id = 'C010'), 3, 900.00, 0.00, 2700.00),
(20240107, (SELECT product_key FROM dim_product WHERE product_id = 'P007'), (SELECT customer_key FROM dim_customer WHERE customer_id = 'C001'), 1, 8000.00, 0.00, 8000.00),
(20240107, (SELECT product_key FROM dim_product WHERE product_id = 'P009'), (SELECT customer_key FROM dim_customer WHERE customer_id = 'C005'), 2, 18000.00, 0.00, 36000.00),
(20240107, (SELECT product_key FROM dim_product WHERE product_id = 'P013'), (SELECT customer_key FROM dim_customer WHERE customer_id = 'C012'), 4, 3200.00, 50.00, 12750.00),
(20240108, (SELECT product_key FROM dim_product WHERE product_id = 'P003'), (SELECT customer_key FROM dim_customer WHERE customer_id = 'C006'), 1, 45000.00, 1350.00, 43650.00),
(20240108, (SELECT product_key FROM dim_product WHERE product_id = 'P012'), (SELECT customer_key FROM dim_customer WHERE customer_id = 'C003'), 4, 650.00, 0.00, 2600.00),
(20240109, (SELECT product_key FROM dim_product WHERE product_id = 'P014'), (SELECT customer_key FROM dim_customer WHERE customer_id = 'C004'), 4, 450.00, 0.00, 1800.00),
(20240110, (SELECT product_key FROM dim_product WHERE product_id = 'P010'), (SELECT customer_key FROM dim_customer WHERE customer_id = 'C007'), 2, 1200.00, 20.00, 2380.00),
(20240111, (SELECT product_key FROM dim_product WHERE product_id = 'P012'), (SELECT customer_key FROM dim_customer WHERE customer_id = 'C002'), 3, 650.00, 0.00, 1950.00),
(20240112, (SELECT product_key FROM dim_product WHERE product_id = 'P001'), (SELECT customer_key FROM dim_customer WHERE customer_id = 'C009'), 1, 100000.00, 7000.00, 93000.00),
(20240112, (SELECT product_key FROM dim_product WHERE product_id = 'P013'), (SELECT customer_key FROM dim_customer WHERE customer_id = 'C008'), 1, 3200.00, 0.00, 3200.00),
(20240113, (SELECT product_key FROM dim_product WHERE product_id = 'P002'), (SELECT customer_key FROM dim_customer WHERE customer_id = 'C004'), 2, 99000.00, 9900.00, 188100.00),
(20240113, (SELECT product_key FROM dim_product WHERE product_id = 'P008'), (SELECT customer_key FROM dim_customer WHERE customer_id = 'C011'), 1, 12000.00, 600.00, 11400.00),
(20240113, (SELECT product_key FROM dim_product WHERE product_id = 'P011'), (SELECT customer_key FROM dim_customer WHERE customer_id = 'C007'), 6, 900.00, 100.00, 5300.00),
(20240114, (SELECT product_key FROM dim_product WHERE product_id = 'P003'), (SELECT customer_key FROM dim_customer WHERE customer_id = 'C012'), 2, 45000.00, 4500.00, 85500.00),
(20240114, (SELECT product_key FROM dim_product WHERE product_id = 'P006'), (SELECT customer_key FROM dim_customer WHERE customer_id = 'C003'), 2, 4000.00, 0.00, 8000.00),
(20240114, (SELECT product_key FROM dim_product WHERE product_id = 'P014'), (SELECT customer_key FROM dim_customer WHERE customer_id = 'C010'), 2, 450.00, 0.00, 900.00),
(20240115, (SELECT product_key FROM dim_product WHERE product_id = 'P010'), (SELECT customer_key FROM dim_customer WHERE customer_id = 'C001'), 1, 1200.00, 0.00, 1200.00),
(20240201, (SELECT product_key FROM dim_product WHERE product_id = 'P011'), (SELECT customer_key FROM dim_customer WHERE customer_id = 'C002'), 2, 900.00, 0.00, 1800.00),
(20240202, (SELECT product_key FROM dim_product WHERE product_id = 'P013'), (SELECT customer_key FROM dim_customer WHERE customer_id = 'C005'), 1, 3200.00, 96.00, 3104.00),
(20240203, (SELECT product_key FROM dim_product WHERE product_id = 'P001'), (SELECT customer_key FROM dim_customer WHERE customer_id = 'C008'), 2, 100000.00, 0.00, 200000.00),
(20240203, (SELECT product_key FROM dim_product WHERE product_id = 'P005'), (SELECT customer_key FROM dim_customer WHERE customer_id = 'C007'), 3, 3500.00, 0.00, 10500.00),
(20240203, (SELECT product_key FROM dim_product WHERE product_id = 'P012'), (SELECT customer_key FROM dim_customer WHERE customer_id = 'C003'), 5, 650.00, 50.00, 3200.00),
(20240204, (SELECT product_key FROM dim_product WHERE product_id = 'P002'), (SELECT customer_key FROM dim_customer WHERE customer_id = 'C009'), 1, 99000.00, 9900.00, 89100.00),
(20240204, (SELECT product_key FROM dim_product WHERE product_id = 'P009'), (SELECT customer_key FROM dim_customer WHERE customer_id = 'C006'), 2, 18000.00, 1800.00, 34200.00),
(20240205, (SELECT product_key FROM dim_product WHERE product_id = 'P010'), (SELECT customer_key FROM dim_customer WHERE customer_id = 'C012'), 2, 1200.00, 0.00, 2400.00),
(20240207, (SELECT product_key FROM dim_product WHERE product_id = 'P004'), (SELECT customer_key FROM dim_customer WHERE customer_id = 'C002'), 1, 2500.00, 0.00, 2500.00),
(20240209, (SELECT product_key FROM dim_product WHERE product_id = 'P012'), (SELECT customer_key FROM dim_customer WHERE customer_id = 'C011'), 3, 650.00, 20.00, 1930.00),
(20240210, (SELECT product_key FROM dim_product WHERE product_id = 'P008'), (SELECT customer_key FROM dim_customer WHERE customer_id = 'C010'), 2, 12000.00, 0.00, 24000.00),
(20240210, (SELECT product_key FROM dim_product WHERE product_id = 'P011'), (SELECT customer_key FROM dim_customer WHERE customer_id = 'C001'), 4, 900.00, 0.00, 3600.00),
(20240211, (SELECT product_key FROM dim_product WHERE product_id = 'P003'), (SELECT customer_key FROM dim_customer WHERE customer_id = 'C004'), 1, 45000.00, 2250.00, 42750.00),
(20240211, (SELECT product_key FROM dim_product WHERE product_id = 'P007'), (SELECT customer_key FROM dim_customer WHERE customer_id = 'C006'), 2, 8000.00, 800.00, 15200.00),
(20240212, (SELECT product_key FROM dim_product WHERE product_id = 'P014'), (SELECT customer_key FROM dim_customer WHERE customer_id = 'C007'), 2, 450.00, 0.00, 900.00),
(20240213, (SELECT product_key FROM dim_product WHERE product_id = 'P015'), (SELECT customer_key FROM dim_customer WHERE customer_id = 'C003'), 1, 100.00, 10.00, 90.00),
(20240215, (SELECT product_key FROM dim_product WHERE product_id = 'P012'), (SELECT customer_key FROM dim_customer WHERE customer_id = 'C008'), 3, 650.00, 50.00, 1900.00)
;
