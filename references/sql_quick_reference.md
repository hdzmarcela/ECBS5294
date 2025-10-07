# SQL Quick Reference

**For:** ECBS5294 - Day 1, Block B: SQL with DuckDB

---

## 📐 SQL Query Structure

```sql
SELECT column1, column2, calculation AS alias
FROM table_name
WHERE row_conditions
GROUP BY column1, column2
HAVING group_conditions
ORDER BY column1 [ASC|DESC]
LIMIT n
```

### Execution Order (Not the same as written order!)
1. **FROM** - Get the table
2. **WHERE** - Filter rows
3. **GROUP BY** - Create groups
4. **HAVING** - Filter groups
5. **SELECT** - Choose columns
6. **ORDER BY** - Sort results
7. **LIMIT** - Restrict count

**Key insight:** WHERE happens before GROUP BY, HAVING happens after!

---

## 🔍 SELECT Basics

```sql
-- Specific columns
SELECT column1, column2 FROM table;

-- All columns
SELECT * FROM table;

-- With aliases
SELECT column1 AS col1, Price * Quantity AS revenue FROM table;

-- Distinct values
SELECT DISTINCT category FROM table;
```

---

## ⚖️ WHERE Clause - Filter Rows

### Comparison Operators
| Operator | Meaning | Example |
|----------|---------|---------|
| `=` | Equal | `WHERE price = 5.00` |
| `!=` or `<>` | Not equal | `WHERE category != 'Coffee'` |
| `>` | Greater than | `WHERE quantity > 10` |
| `<` | Less than | `WHERE price < 5.00` |
| `>=` | Greater or equal | `WHERE quantity >= 5` |
| `<=` | Less or equal | `WHERE price <= 10.00` |

### Logical Operators
```sql
-- AND (both conditions must be true)
WHERE price > 5 AND category = 'Coffee'

-- OR (either condition can be true)
WHERE category = 'Coffee' OR category = 'Tea'

-- NOT
WHERE NOT category = 'Coffee'
```

### Special Operators
```sql
-- IN (matches any value in list)
WHERE country IN ('France', 'Germany', 'Spain')

-- BETWEEN (inclusive range)
WHERE price BETWEEN 3.00 AND 7.00

-- LIKE (pattern matching)
WHERE product LIKE '%Latte%'  -- Contains "Latte"
WHERE product LIKE 'Latte%'   -- Starts with "Latte"
WHERE product LIKE '%Latte'   -- Ends with "Latte"
-- Wildcards: % = any characters, _ = one character
```

---

## 🚨 NULL Handling (CRITICAL!)

```sql
-- ❌ WRONG - This NEVER works!
WHERE column = NULL     -- Always returns 0 rows

-- ✅ CORRECT
WHERE column IS NULL
WHERE column IS NOT NULL
```

**Key Rules:**
- NULL is NOT equal to anything (not even NULL)
- Use `IS NULL` or `IS NOT NULL`
- Comparison operators (`>`, `<`, `=`) automatically exclude NULLs
- `COUNT(column)` excludes NULLs, but `COUNT(*)` includes them

---

## 📊 Aggregate Functions

| Function | What it does | NULL behavior |
|----------|--------------|---------------|
| `COUNT(*)` | Counts all rows | Includes NULLs |
| `COUNT(column)` | Counts non-NULL values | Excludes NULLs |
| `SUM(column)` | Adds up values | Excludes NULLs |
| `AVG(column)` | Average | Excludes NULLs |
| `MIN(column)` | Smallest value | Excludes NULLs |
| `MAX(column)` | Largest value | Excludes NULLs |

```sql
SELECT
    COUNT(*) AS total_rows,
    COUNT(payment_method) AS with_payment,
    SUM(price * quantity) AS revenue,
    AVG(price) AS avg_price,
    MIN(price) AS min_price,
    MAX(price) AS max_price
FROM sales;
```

---

## 👥 GROUP BY

```sql
SELECT
    category,
    COUNT(*) AS transaction_count,
    SUM(price * quantity) AS revenue
FROM sales
GROUP BY category
ORDER BY revenue DESC;
```

**Rules:**
- Every column in SELECT must be either:
  1. In the GROUP BY clause, OR
  2. Inside an aggregate function
- GROUP BY collapses rows (one row per group)

```sql
-- ❌ WRONG - price not in GROUP BY or aggregated
SELECT category, price, COUNT(*)
FROM sales
GROUP BY category

-- ✅ CORRECT
SELECT category, AVG(price), COUNT(*)
FROM sales
GROUP BY category
```

---

## ⚔️ WHERE vs HAVING

| | WHERE | HAVING |
|---|-------|--------|
| **Filters** | Individual rows | Groups (after aggregation) |
| **When** | Before GROUP BY | After GROUP BY |
| **Can use aggregates?** | ❌ No | ✅ Yes |
| **Example** | `WHERE price > 5` | `HAVING COUNT(*) > 100` |

```sql
-- Example using both
SELECT
    category,
    COUNT(*) AS transaction_count,
    AVG(price) AS avg_price
FROM sales
WHERE price > 5              -- Filter rows first
GROUP BY category
HAVING COUNT(*) > 100        -- Filter groups after
ORDER BY transaction_count DESC;
```

**Decision:** Filtering rows? → WHERE. Filtering groups? → HAVING.

---

## 🪟 Window Functions

**Key difference:** Window functions preserve rows; GROUP BY collapses rows.

### Basic Syntax
```sql
<function>() OVER (
    [PARTITION BY column]    -- Optional: groups
    [ORDER BY column]        -- Optional: order
    [ROWS BETWEEN ...]       -- Optional: frame
)
```

### Common Functions

**1. ROW_NUMBER() - Ranking/Latest per group**
```sql
-- Latest order per customer
SELECT * FROM (
    SELECT
        customer_id,
        order_date,
        ROW_NUMBER() OVER (
            PARTITION BY customer_id
            ORDER BY order_date DESC
        ) AS row_num
    FROM orders
)
WHERE row_num = 1;
```

**2. LAG/LEAD - Row-to-row comparison**
```sql
-- Month-over-month change
SELECT
    month,
    revenue,
    LAG(revenue, 1) OVER (ORDER BY month) AS prev_month_revenue,
    revenue - LAG(revenue, 1) OVER (ORDER BY month) AS change
FROM monthly_sales
ORDER BY month;
```

**3. Moving Average - Smoothing**
```sql
-- 7-day moving average
SELECT
    date,
    daily_sales,
    AVG(daily_sales) OVER (
        ORDER BY date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS moving_avg_7day
FROM daily_sales;
```

### Frame Specifications
```sql
ROWS BETWEEN 6 PRECEDING AND CURRENT ROW        -- 7 rows (6 + current)
ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING        -- 3 rows
ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW  -- Running total
```

---

## 🔀 ORDER BY

```sql
-- Ascending (default)
SELECT * FROM sales ORDER BY price;
SELECT * FROM sales ORDER BY price ASC;

-- Descending
SELECT * FROM sales ORDER BY price DESC;

-- Multiple columns (first priority, then second, ...)
SELECT * FROM sales ORDER BY category ASC, price DESC;

-- By calculated column
SELECT price * quantity AS revenue
FROM sales
ORDER BY revenue DESC;
```

---

## 🎯 Common Patterns

### Top N per Group
```sql
-- Top 3 products per category by revenue
SELECT * FROM (
    SELECT
        category,
        product,
        revenue,
        ROW_NUMBER() OVER (
            PARTITION BY category
            ORDER BY revenue DESC
        ) AS rank
    FROM products
)
WHERE rank <= 3;
```

### Running Total
```sql
SELECT
    date,
    daily_sales,
    SUM(daily_sales) OVER (
        ORDER BY date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_total
FROM sales;
```

### Percent of Total
```sql
SELECT
    category,
    SUM(revenue) AS category_revenue,
    ROUND(
        100.0 * SUM(revenue) / SUM(SUM(revenue)) OVER (),
        2
    ) AS pct_of_total
FROM sales
GROUP BY category;
```

---

## 🦆 DuckDB-Specific Features

### Query Files Directly
```sql
-- No need to load - query CSV/Parquet directly!
SELECT * FROM 'data/sales.csv' LIMIT 10;
SELECT * FROM 'data/sales.parquet' WHERE category = 'Coffee';
```

### Convert to DataFrame
```python
import duckdb
con = duckdb.connect(':memory:')
result = con.execute("SELECT * FROM 'file.csv'").df()  # Returns pandas DataFrame
```

### Date Functions
```sql
DATE_TRUNC('month', date_column)  -- First day of month
DATE_TRUNC('week', date_column)   -- First day of week
EXTRACT(YEAR FROM date_column)    -- Get year
CAST(datetime_column AS DATE)     -- Convert to date only
```

---

## 🐛 Debugging Tips

**Query not working?**
1. Start simple: `SELECT * FROM table LIMIT 5`
2. Add WHERE one condition at a time
3. Check for NULLs: `SELECT COUNT(*), COUNT(column) FROM table`
4. Verify data types: Look at the data!
5. Use LIMIT while developing

**Common errors:**
- **"Column not found"** → Check spelling, check case
- **"Cannot use aggregate"** → Use HAVING, not WHERE
- **"Column must appear in GROUP BY"** → Add to GROUP BY or wrap in aggregate
- **Query returns 0 rows** → Check for `= NULL` (should be `IS NULL`)

---

## 💡 Best Practices

**Formatting:**
```sql
-- ✅ Good: Readable
SELECT
    category,
    COUNT(*) AS count,
    SUM(revenue) AS total_revenue
FROM sales
WHERE price > 5
GROUP BY category
HAVING COUNT(*) > 100
ORDER BY total_revenue DESC;

-- ❌ Bad: Hard to read
select category,count(*),sum(revenue) from sales where price>5 group by category having count(*)>100 order by 3 desc;
```

**Tips:**
- Uppercase SQL keywords (`SELECT`, `FROM`, `WHERE`)
- Indent for readability
- Use meaningful aliases
- Comment complex queries
- Use LIMIT while developing
- Check for NULLs early
- Build queries incrementally

---

## 📚 Quick Decision Trees

### "Should I use WHERE or HAVING?"
- Filtering individual rows? → **WHERE**
- Filtering aggregated results? → **HAVING**

### "Should I use GROUP BY or window function?"
- Want summary only (fewer rows)? → **GROUP BY**
- Want detail + calculation (same rows)? → **Window function**

### "How do I check for missing values?"
- Use `IS NULL`, never `= NULL`!

---

**Remember:** SQL is about declaring WHAT you want, not HOW to get it. The database figures out the optimal execution!

**Practice makes perfect!** The more you write SQL, the more natural it becomes. 🚀
