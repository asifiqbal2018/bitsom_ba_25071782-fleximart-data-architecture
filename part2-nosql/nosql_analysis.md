# FlexiMart – NoSQL Database Analysis (MongoDB)

## Section A: Limitations of RDBMS (≈150 words)

The current relational database design works well when product records look similar, but it struggles when products have **highly diverse attributes**. For example, a laptop needs fields like RAM, processor, screen_size, and battery_life, while shoes need size, color, material, and fit_type. In an RDBMS, handling this usually means either adding many optional columns (causing lots of NULLs and wasted space) or creating many subtype tables (laptops table, shoes table, etc.), which increases complexity and join operations.

Frequent schema changes are another issue: whenever FlexiMart adds a new product type or attribute, the database schema must be altered, which can require migrations, downtime, and code updates. Also, customer reviews are naturally **nested** (each product has many reviews with rating, comment, reviewer info, timestamps). In SQL, reviews typically become a separate table requiring joins, making retrieval of a “product + all reviews” slower and more complex.

---

## Section B: NoSQL Benefits (≈150 words)

MongoDB is well-suited for a diverse product catalog because it supports a **flexible schema** using JSON-like documents. Each product document can store only the attributes it needs. A laptop document can include RAM and processor fields, while a shoe document can include size and color fields, without altering a global schema or creating multiple subtype tables. This reduces NULL-heavy designs and avoids repeated schema migrations when new product attributes appear.

MongoDB also supports **embedded documents**, which makes it easy to store customer reviews directly inside the product document as an array (e.g., reviews: [{rating, comment, user, date}, ...]). This is ideal when the application frequently displays a product along with its reviews, because a single document read returns everything needed without joins.

Additionally, MongoDB is designed for **horizontal scalability** through sharding. As the catalog grows (more products, more reviews, more traffic), MongoDB can distribute data across multiple servers, improving performance and supporting large-scale growth more easily than many traditional single-node SQL setups.

---

## Section C: Trade-offs (≈100 words)

Two disadvantages of using MongoDB instead of a relational database are:

1) **Weaker relational integrity by default:** In SQL, foreign keys enforce consistent relationships (e.g., order_items must reference a valid product). MongoDB does not enforce foreign keys in the same way, so the application must handle validation and consistency rules, which increases responsibility on developers.

2) **More complex multi-document transactions and reporting:** While MongoDB supports transactions, SQL databases are still stronger and simpler for complex reporting queries with multiple joins and strict ACID guarantees. Aggregations across many collections can be harder to write and tune compared to SQL analytics, especially when you need highly structured business reporting.
