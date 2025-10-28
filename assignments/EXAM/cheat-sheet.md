### Section 1: BASIC SELECT + FILTERING PATTERNS

~~~
con.execute("""
SELECT
    order_id,                           -- select columns
    customer_id,
    order_status
FROM orders                             -- *fact table: one order per row*
WHERE
      order_status = 'delivered'        -- exact match filter
  AND customer_id IS NOT NULL           -- remove missing ids
  AND order_purchase_timestamp BETWEEN
      '2017-01-01' AND '2017-12-31'     -- date range filter
  AND order_status IN ('delivered', 'shipped')  -- match multiple categories
ORDER BY order_purchase_timestamp DESC    -- sort latest orders first
LIMIT 10;  
""").df() -- preview results
~~~

### Group by Aggregations

~~~
SELECT
    c.customer_state,                   -- *group column (dimension)*
    COUNT(o.order_id)        AS n_orders,    -- count rows
    AVG(o.payment_installments) AS avg_installments,  -- mean
    MIN(o.order_purchase_timestamp) AS first_order,   -- earliest date
    MAX(o.order_purchase_timestamp) AS latest_order   -- latest date
FROM orders o                       -- *fact table: one row per order*
JOIN customers c                    -- join to add grouping dimension
  ON o.customer_id = c.customer_id      -- *foreign key join*
WHERE o.order_status = 'delivered'  -- row filter BEFORE aggregation
GROUP BY c.customer_state           -- group by dimension
HAVING COUNT(o.order_id) > 50       -- filter groups AFTER aggregation
ORDER BY n_orders DESC;             -- sort aggregated output
~~~

### Windows

~~~
Top product by revenue (per product or overall) — if used in your class:
WITH order_rev AS (             -- *items → order level metric*
    SELECT
        product_id,     
        SUM(price + freight_value) AS total_rev
    FROM order_items
    GROUP BY product_id
)
SELECT
    product_id,
    total_rev,
    ROW_NUMBER() OVER (ORDER BY total_rev DESC) AS rn_overall  -- *rank highest first*
FROM order_rev
ORDER BY total_rev DESC
LIMIT 10;         -- *preview top products*
~~~

---

### 2. JOIN PATTERNS

~~~
-- INNER JOIN → keep matching rows only
SELECT
    o.order_id,                 -- *main entity: order*
    o.customer_id,
    c.customer_state.           -- *dimension from customers*
FROM orders o                   -- *fact table: orders*
INNER JOIN customers c          -- combine with customer info
    ON o.customer_id = c.customer_id   -- *foreign key join condition*
WHERE o.order_status = 'delivered';

-- LEFT JOIN → keep all rows from left table, even if no match
SELECT
    c.customer_id,               -- *left table preserved*
    c.customer_state,
    o.order_id                   -- *may become NULL if no match*
FROM customers c                 -- *customer base table*
LEFT JOIN orders o                              
    ON c.customer_id = o.customer_id   -- *same key as above*
ORDER BY c.customer_id;

-- MULTI-TABLE JOIN → orders + customers + order_items
SELECT
    o.order_id,
    c.customer_state,
    oi.product_id,
    oi.price
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id -- *add customer info*
JOIN order_items oi ON o.order_id = oi.order_id -- *attach items 2order*
LIMIT 10;                                          
~~~

### CTE PIPELINE PATTERN

~~~

WITH order_value AS (        -- *Step 1: calc order revenue*
    SELECT
        order_id,                  -- join key
        SUM(price + freight_value) AS order_revenue   -- revenue per order
    FROM order_items               -- *one row per item*
    GROUP BY order_id
),
customer_value AS (                -- *Step 2: aggregate to customer*
    SELECT
        o.customer_id,                   -- group key
        SUM(ov.order_revenue) AS customer_revenue,  -- sum orders per customer
        COUNT(o.order_id) AS n_orders            -- number of orders
    FROM orders o                                -- start at orders table
    JOIN order_value ov                          -- join CTE from Step 1
      ON o.order_id = ov.order_id
    GROUP BY o.customer_id
)
SELECT *                                         -- *Step 3: final output*
FROM customer_value
WHERE n_orders >= 3                              -- filter heavy buyers
ORDER BY customer_revenue DESC;
~~~

### DATE FUNCTIONS

~~~
-- Convert timestamp to month buckets
SELECT                                   -- *truncate to month*
    DATE_TRUNC('month', order_purchase_timestamp) AS order_month,
    COUNT(*) AS n_orders               -- *monthly order count*
FROM orders
GROUP BY order_month
ORDER BY order_month;

-- Filter by date range (inclusive)
SELECT
    order_id,
    order_purchase_timestamp
FROM orders
WHERE order_purchase_timestamp BETWEEN
      '2017-06-01' AND '2017-06-30';     -- *range filter*
~~~

### SUBQUERY PATTERN

~~~~
-- Use subquery to filter original table
SELECT
    order_id,
    customer_id
FROM orders
WHERE customer_id IN (             -- *subquery list filter*
    SELECT customer_id
    FROM orders
    GROUP BY customer_id
    HAVING COUNT(*) >= 5           -- *active Repeat Buyers*
);
~~~~

### JSON

~~~

CREATE TABLE permits AS
SELECT * FROM read_json_auto('path');  -- *auto-detect schema*

-- Extract JSON fields
SELECT
    json_extract(value, '$.job_number')    AS job_number,      -- *class example*
    json_extract(value, '$.permit_type')   AS permit_type
FROM permits
LIMIT 10;
~~~

---

#### PIPELINE ARCHITECTURE

~~~

-- BRONZE = raw load
CREATE TABLE bronze_orders AS
SELECT * FROM 'data/day3/teaching/olist_orders_subset.csv';

-- SILVER = typed + cleaned
CREATE TABLE silver_orders AS
SELECT
    CAST(order_id AS VARCHAR) AS order_id,                 -- *type cast*
    CAST(customer_id AS VARCHAR) AS customer_id,
    CAST(order_purchase_timestamp AS TIMESTAMP) AS order_ts
FROM bronze_orders;

-- GOLD = analysis-ready
CREATE TABLE gold_orders_by_state_month AS
SELECT
    c.customer_state,                                      -- *dimension*
    DATE_TRUNC('month', o.order_ts) AS order_month,        -- *time grouping*
    COUNT(*) AS n_orders                                   -- *fact metric*
FROM silver_orders o
JOIN customers c ON o.customer_id = c.customer_id
GROUP BY c.customer_state, order_month;
~~~
