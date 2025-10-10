# Day 2 Datasets

This directory contains datasets used in Day 2 teaching materials.

---

## Block A: Brazilian E-Commerce (Olist)

**Source:** Kaggle - Brazilian E-Commerce Public Dataset by Olist
**URL:** https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
**License:** CC BY-NC-SA 4.0
**Used in:** Day 2 Block A (SQL Joins and Multi-Table Queries)

---

## Dataset Description

This is a **real-world Brazilian e-commerce dataset** containing 100,000 orders made at the Olist Store between 2016 and 2018. Olist is the largest department store marketplace in Brazil, connecting small businesses to customers through a single contract.

This dataset is perfect for teaching SQL joins because it contains **multiple interconnected tables** with clear primary key/foreign key relationships. Students will learn to combine data from customers, orders, products, sellers, payments, and reviews to answer business questions.

**Why this dataset?**
- ✅ Real business data from actual e-commerce marketplace
- ✅ Multiple tables with clear relationships (like production databases)
- ✅ Complex enough to teach all join types (INNER, LEFT, RIGHT, FULL)
- ✅ Business-relevant questions: customer behavior, product performance, seller analysis
- ✅ Data quality issues to handle (nulls, missing relationships)

---

## Dataset Structure

### Core Tables (Primary Focus for Day 2)

#### 1. `olist_orders_dataset.csv` - Orders (Fact Table)
**99,441 orders** | Primary Key: `order_id`

| Column | Type | Description |
|--------|------|-------------|
| `order_id` | string | Unique order identifier (PK) |
| `customer_id` | string | Foreign key to customers table |
| `order_status` | string | Order status (delivered, shipped, canceled, etc.) |
| `order_purchase_timestamp` | datetime | When order was placed |
| `order_approved_at` | datetime | When payment was approved |
| `order_delivered_carrier_date` | datetime | When order handed to carrier |
| `order_delivered_customer_date` | datetime | When order delivered to customer |
| `order_estimated_delivery_date` | datetime | Estimated delivery date shown to customer |

**Business value:** Central fact table connecting customers, order items, payments, and reviews.

---

#### 2. `olist_customers_dataset.csv` - Customers (Dimension Table)
**99,441 customers** | Primary Key: `customer_id`

| Column | Type | Description |
|--------|------|-------------|
| `customer_id` | string | Unique customer identifier (PK) |
| `customer_unique_id` | string | Unique identifier for customer (handles duplicates) |
| `customer_zip_code_prefix` | integer | First 5 digits of ZIP code |
| `customer_city` | string | Customer city |
| `customer_state` | string | Customer state (2-letter code) |

**Business value:** Who are our customers? Where do they live? Customer segmentation by location.

**Note:** `customer_id` is unique per order, but `customer_unique_id` identifies the same person across multiple orders.

---

#### 3. `olist_order_items_dataset.csv` - Order Line Items (Fact Table)
**112,650 order items** | Composite Key: `order_id` + `order_item_id`

| Column | Type | Description |
|--------|------|-------------|
| `order_id` | string | Foreign key to orders table |
| `order_item_id` | integer | Sequential item number within order (1, 2, 3...) |
| `product_id` | string | Foreign key to products table |
| `seller_id` | string | Foreign key to sellers table |
| `shipping_limit_date` | datetime | Seller must ship by this date |
| `price` | float | Item price in BRL (Brazilian Real) |
| `freight_value` | float | Shipping cost in BRL |

**Business value:** What products were ordered? How much revenue per order? Which sellers fulfilled items?

**Important:** One order can contain multiple items. This creates a **one-to-many relationship** with orders.

---

#### 4. `olist_products_dataset.csv` - Products (Dimension Table)
**32,951 products** | Primary Key: `product_id`

| Column | Type | Description |
|--------|------|-------------|
| `product_id` | string | Unique product identifier (PK) |
| `product_category_name` | string | Product category (in Portuguese) |
| `product_name_lenght` | integer | Number of characters in product name |
| `product_description_lenght` | integer | Number of characters in description |
| `product_photos_qty` | integer | Number of product photos |
| `product_weight_g` | integer | Product weight in grams |
| `product_length_cm` | integer | Product length in cm |
| `product_height_cm` | integer | Product height in cm |
| `product_width_cm` | integer | Product width in cm |

**Business value:** What products do we sell? Product catalog analysis, category performance.

**Note:** Actual product names are anonymized. Category names are in Portuguese (use translation table).

---

#### 5. `olist_sellers_dataset.csv` - Sellers (Dimension Table)
**3,095 sellers** | Primary Key: `seller_id`

| Column | Type | Description |
|--------|------|-------------|
| `seller_id` | string | Unique seller identifier (PK) |
| `seller_zip_code_prefix` | integer | First 5 digits of ZIP code |
| `seller_city` | string | Seller city |
| `seller_state` | string | Seller state (2-letter code) |

**Business value:** Who are our sellers? Where are they located? Seller performance by region.

---

### Supporting Tables (For Advanced Exercises)

#### 6. `olist_order_payments_dataset.csv` - Payments
**103,886 payment transactions** | Composite Key: `order_id` + `payment_sequential`

| Column | Type | Description |
|--------|------|-------------|
| `order_id` | string | Foreign key to orders table |
| `payment_sequential` | integer | Payment number (1, 2, 3 if multiple payments) |
| `payment_type` | string | Payment method (credit_card, boleto, voucher, debit_card) |
| `payment_installments` | integer | Number of installments |
| `payment_value` | float | Payment amount in BRL |

**Business value:** How do customers pay? Are installments common? What's the total payment per order?

**Note:** One order can have multiple payment methods (e.g., 50% credit card, 50% voucher).

---

#### 7. `olist_order_reviews_dataset.csv` - Reviews
**104,719 reviews** | Primary Key: `review_id`

| Column | Type | Description |
|--------|------|-------------|
| `review_id` | string | Unique review identifier (PK) |
| `order_id` | string | Foreign key to orders table |
| `review_score` | integer | Rating from 1 (worst) to 5 (best) |
| `review_comment_title` | string | Review title (Portuguese) |
| `review_comment_message` | string | Review text (Portuguese) |
| `review_creation_date` | datetime | When review was created |
| `review_answer_timestamp` | datetime | When review was answered |

**Business value:** Customer satisfaction, sentiment analysis, product quality feedback.

---

#### 8. `product_category_name_translation.csv` - Category Translation
**71 categories** | Primary Key: `product_category_name`

| Column | Type | Description |
|--------|------|-------------|
| `product_category_name` | string | Category name in Portuguese (PK) |
| `product_category_name_english` | string | Category name in English |

**Business value:** Translate Portuguese category names to English for analysis.

**Examples:**
- `perfumaria` → `perfumery`
- `moveis_decoracao` → `furniture_decor`
- `informatica_acessorios` → `computers_accessories`

---

#### 9. `olist_geolocation_dataset.csv` - Geolocation (Optional)
**1,000,163 geolocation records** | Composite Key: `geolocation_zip_code_prefix` + `geolocation_lat` + `geolocation_lng`

| Column | Type | Description |
|--------|------|-------------|
| `geolocation_zip_code_prefix` | integer | First 5 digits of ZIP code |
| `geolocation_lat` | float | Latitude |
| `geolocation_lng` | float | Longitude |
| `geolocation_city` | string | City name |
| `geolocation_state` | string | State (2-letter code) |

**Business value:** Map customer and seller locations, calculate distances, logistics analysis.

**Note:** This table is LARGE (1M rows) and optional for Day 2. Use for advanced geospatial exercises.

---

## Entity-Relationship Diagram

```
┌─────────────────┐
│   customers     │
│  (99,441)       │
│                 │
│ customer_id (PK)│───┐
└─────────────────┘   │
                      │
                      │
┌─────────────────┐   │    ┌──────────────────┐
│   orders        │   │    │  order_items     │
│  (99,441)       │   │    │  (112,650)       │
│                 │   │    │                  │
│ order_id (PK)   │◄──┼────│ order_id (FK)    │
│ customer_id(FK) │◄──┘    │ product_id (FK)  │───┐
└─────────────────┘        │ seller_id (FK)   │───┼───┐
       ▲                   └──────────────────┘   │   │
       │                                           │   │
       │                                           │   │
       │                   ┌──────────────────┐   │   │
       │                   │   products       │   │   │
       │                   │  (32,951)        │   │   │
       │                   │                  │   │   │
       │                   │ product_id (PK)  │◄──┘   │
       │                   └──────────────────┘       │
       │                                               │
       │                   ┌──────────────────┐       │
       │                   │   sellers        │       │
       │                   │  (3,095)         │       │
       │                   │                  │       │
       │                   │ seller_id (PK)   │◄──────┘
       │                   └──────────────────┘
       │
       │
       ├───────────────────┐
       │                   │
       │                   │
┌──────▼──────────┐  ┌─────▼────────────┐
│  payments       │  │   reviews        │
│  (103,886)      │  │  (104,719)       │
│                 │  │                  │
│ order_id (FK)   │  │ order_id (FK)    │
└─────────────────┘  └──────────────────┘
```

**Key Relationships:**
- One customer → Many orders (via `customer_id`)
- One order → Many order items (via `order_id`)
- One order → Many payments (via `order_id`)
- One order → One or more reviews (via `order_id`)
- One product → Many order items (via `product_id`)
- One seller → Many order items (via `seller_id`)

---

## Recommended Tables for Day 2 Teaching

**Start with these 4 core tables:**

1. **`olist_orders_dataset.csv`** - Central fact table
2. **`olist_customers_dataset.csv`** - Who placed orders?
3. **`olist_order_items_dataset.csv`** - What was ordered?
4. **`olist_products_dataset.csv`** - Product catalog

**Why these 4?**
- Clear primary key/foreign key relationships
- Teach all join types (INNER, LEFT, RIGHT, FULL)
- Answer real business questions
- Manageable size (combined ~250K rows)

**Add for advanced exercises:**
- `olist_sellers_dataset.csv` - Multi-table joins (orders → items → sellers)
- `olist_order_payments_dataset.csv` - Multiple payments per order
- `olist_order_reviews_dataset.csv` - Customer satisfaction analysis
- `product_category_name_translation.csv` - String joins

---

## Intentional Data Characteristics

### Good News (Clean Data)
- ✅ No duplicate primary keys
- ✅ Consistent data types
- ✅ Valid date ranges (2016-2018)
- ✅ Clear foreign key relationships

### Teaching Opportunities (Real-World Messiness)

**1. Unmatched Rows (Perfect for JOIN Teaching!)**
- ❓ **Do all products appear in order_items?** NO! Some products have never been ordered.
  - Use case: `LEFT JOIN` to find products with zero sales
- ❓ **Do all customers have orders?** YES (by design - customer_id created at order time)
- ❓ **Do all orders have reviews?** NO! ~95% of orders have reviews, but ~5% don't.
  - Use case: `LEFT JOIN` to find orders without reviews

**2. Null Values**
- `order_approved_at`: NULL if payment not approved yet
- `order_delivered_carrier_date`: NULL if not shipped
- `order_delivered_customer_date`: NULL if not delivered
- `product_category_name`: Some products have NULL categories
- `review_comment_title`, `review_comment_message`: Many reviews have no text (just score)

**3. One-to-Many Relationships**
- One order → Multiple items (avg ~1.13 items per order)
- One order → Multiple payments (some customers split payment)
- **Watch for duplicate rows!** Joining orders to order_items inflates row count.

**4. Data Quality Issues**
- Some `product_id` in order_items don't exist in products table (orphaned FKs)
- Some `seller_id` in order_items don't exist in sellers table
- **Pedagogical gold:** Students must decide how to handle with different join types

---

## Learning Objectives

By working with this dataset, students will practice:

### Block A: SQL Joins (Day 2 Focus)

**Core Concepts:**
1. **INNER JOIN** - Only matching rows from both tables
   - Example: Orders with products (only completed orders with valid products)
2. **LEFT JOIN** - All rows from left table + matches from right
   - Example: All orders, even those without reviews
3. **RIGHT JOIN** - All rows from right table + matches from left
   - Example: All products, even those never ordered
4. **FULL OUTER JOIN** - All rows from both tables
   - Example: Complete view of orders and reviews (including orphaned records)

**Key Skills:**
- Understanding primary keys and foreign keys
- Recognizing one-to-many relationships
- Handling unmatched rows appropriately
- Avoiding duplicate row inflation
- Aggregating after joins (GROUP BY on the right grain)

**Business Questions:**
- What are the top 10 best-selling products?
- Which customers have placed the most orders?
- Which sellers have the highest average review scores?
- What percentage of orders are delivered on time?
- Which product categories generate the most revenue?

---

## Sample DuckDB Queries

### Load Tables

```sql
-- Load orders
CREATE TABLE orders AS
SELECT * FROM 'data/day2/block_a/olist_orders_dataset.csv';

-- Load customers
CREATE TABLE customers AS
SELECT * FROM 'data/day2/block_a/olist_customers_dataset.csv';

-- Load order items
CREATE TABLE order_items AS
SELECT * FROM 'data/day2/block_a/olist_order_items_dataset.csv';

-- Load products
CREATE TABLE products AS
SELECT * FROM 'data/day2/block_a/olist_products_dataset.csv';

-- Verify row counts
SELECT 'orders' as table_name, COUNT(*) as row_count FROM orders
UNION ALL
SELECT 'customers', COUNT(*) FROM customers
UNION ALL
SELECT 'order_items', COUNT(*) FROM order_items
UNION ALL
SELECT 'products', COUNT(*) FROM products;
```

### Example Joins

**1. INNER JOIN: Orders with customer details**
```sql
SELECT
    o.order_id,
    o.order_purchase_timestamp,
    c.customer_city,
    c.customer_state
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id
LIMIT 10;
```

**2. LEFT JOIN: All orders, even those without reviews**
```sql
-- Load reviews first
CREATE TABLE reviews AS
SELECT * FROM 'data/day2/block_a/olist_order_reviews_dataset.csv';

-- Find orders without reviews
SELECT
    o.order_id,
    o.order_purchase_timestamp,
    r.review_score
FROM orders o
LEFT JOIN reviews r ON o.order_id = r.order_id
WHERE r.review_id IS NULL;
```

**3. Aggregation after JOIN: Revenue by product category**
```sql
-- Join order_items → products → category translation
SELECT
    p.product_category_name,
    COUNT(DISTINCT oi.order_id) as num_orders,
    SUM(oi.price) as total_revenue,
    AVG(oi.price) as avg_item_price
FROM order_items oi
INNER JOIN products p ON oi.product_id = p.product_id
WHERE p.product_category_name IS NOT NULL
GROUP BY p.product_category_name
ORDER BY total_revenue DESC
LIMIT 10;
```

**4. Multi-table JOIN: Orders → Items → Products → Sellers**
```sql
-- Load sellers
CREATE TABLE sellers AS
SELECT * FROM 'data/day2/block_a/olist_sellers_dataset.csv';

-- Top sellers by number of items sold
SELECT
    s.seller_id,
    s.seller_city,
    s.seller_state,
    COUNT(*) as items_sold,
    SUM(oi.price) as total_sales
FROM order_items oi
INNER JOIN sellers s ON oi.seller_id = s.seller_id
GROUP BY s.seller_id, s.seller_city, s.seller_state
ORDER BY total_sales DESC
LIMIT 10;
```

---

## Common Pitfalls & Teaching Notes

### 1. Row Count Explosion
**Problem:** Joining orders (99K rows) to order_items (112K rows) returns 112K rows, not 99K!

**Why:** One order can have multiple items (one-to-many relationship).

**Solution:** Always check row counts before/after joins. Aggregate at the correct grain.

```sql
-- ❌ Wrong: This counts orders multiple times if they have multiple items
SELECT COUNT(*) FROM orders o
INNER JOIN order_items oi ON o.order_id = oi.order_id;
-- Returns 112,650 (number of items, not orders!)

-- ✅ Correct: Count distinct orders
SELECT COUNT(DISTINCT o.order_id) FROM orders o
INNER JOIN order_items oi ON o.order_id = oi.order_id;
-- Returns 99,441 (actual number of orders)
```

### 2. Handling Unmatched Foreign Keys
**Problem:** Some `product_id` in order_items don't exist in products table.

**Decision points for students:**
- INNER JOIN: Exclude these rows (most conservative)
- LEFT JOIN: Keep order_items, show NULL for product info
- Document the issue and explain your choice!

### 3. NULL vs Missing Relationships
**Problem:** `review_score = NULL` could mean two things:
1. Order has no review (no matching row in reviews table)
2. Review exists but score is NULL (unlikely)

**Solution:** Use `IS NULL` checks on the foreign key (`review_id`), not the data columns.

---

## Attribution & License

**License:** CC BY-NC-SA 4.0 (Creative Commons Attribution-NonCommercial-ShareAlike 4.0)

This means:
- ✅ Free to use for educational purposes
- ✅ Can modify and build upon
- ✅ Must give attribution
- ❌ Cannot use commercially
- ❌ Derivatives must use same license

**Required Attribution:**
> Brazilian E-Commerce Public Dataset by Olist. (2018). Retrieved from https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce. Licensed under CC BY-NC-SA 4.0.

**Original Source:** Olist (https://olist.com/pt-br/)

**Published by:** Olist on Kaggle (2018)

---

## Tips for Students

### Start Simple, Build Up
1. **First:** Explore individual tables (SELECT, WHERE, ORDER BY, GROUP BY)
2. **Then:** Join two tables (orders + customers)
3. **Then:** Join three tables (orders + order_items + products)
4. **Finally:** Complex multi-table joins with aggregations

### Validate Your Joins
Always check:
```sql
-- Before join: How many orders?
SELECT COUNT(*) FROM orders;  -- Should be 99,441

-- After join: How many rows?
SELECT COUNT(*) FROM orders o
INNER JOIN order_items oi ON o.order_id = oi.order_id;  -- Should be 112,650

-- Why the difference? One-to-many relationship!
```

### Use Table Aliases
```sql
-- ❌ Hard to read
SELECT order_id FROM orders WHERE order_id = '123';

-- ✅ Clear, especially with multiple tables
SELECT o.order_id, c.customer_city
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id;
```

### Check for Unmatched Rows
```sql
-- Products never ordered (use this pattern for LEFT/RIGHT JOIN practice)
SELECT p.product_id, p.product_category_name
FROM products p
LEFT JOIN order_items oi ON p.product_id = oi.product_id
WHERE oi.order_id IS NULL;
```

---

## Need Help?

**Common issues:**

- **"Too many rows after join!"** → You have a one-to-many relationship. Use `COUNT(DISTINCT ...)` or aggregate at the correct grain.
- **"Some products show NULL"** → Foreign key doesn't exist in dimension table. Decide: INNER JOIN (exclude) or LEFT JOIN (keep with NULLs).
- **"Dates won't parse"** → DuckDB handles this automatically for ISO format. If issues, use `CAST(... AS TIMESTAMP)`.
- **"Category names are in Portuguese"** → Join with `product_category_name_translation.csv`.

**For more examples, see Day 2 teaching notebooks:**
- `notebooks/day2_block_a_01_joins_basics.ipynb`
- `notebooks/day2_block_a_02_join_patterns.ipynb`

---

## Advanced Exercises

Once comfortable with basic joins, try:

1. **Calculate seller performance:**
   - Join: order_items → sellers → reviews
   - Metric: Average review score per seller
   - Filter: Only sellers with 10+ orders

2. **Customer lifetime value:**
   - Join: customers → orders → order_items
   - Metric: Total revenue per customer
   - Rank: Top 100 customers by revenue

3. **Product category trends:**
   - Join: products → order_items → orders
   - Group by: Month and category
   - Visualize: Revenue trends over time

4. **Delivery performance:**
   - Compare `order_estimated_delivery_date` vs `order_delivered_customer_date`
   - Calculate: Percentage on-time delivery by seller
   - Insight: Which sellers consistently deliver on time?

5. **Geographic analysis (use geolocation table):**
   - Join: customers → geolocation
   - Calculate: Distance between customer and seller
   - Insight: How does distance affect delivery time?

---

**Ready to start? Open `notebooks/day2_block_a_01_joins_basics.ipynb` and let's join some tables!**
