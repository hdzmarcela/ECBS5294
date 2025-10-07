---
marp: true
theme: ceu
paginate: true
header: 'Day 1, Block B: SQL Foundations'
footer: 'ECBS5294 | CEU'
---

<!-- _class: lead -->

# Block B
## SQL with DuckDB: Single-Table Mastery

**90 minutes**

---

# What We'll Cover

1. **Why SQL?** (The right tool for the job)
2. **Core SQL:** SELECT, WHERE, ORDER BY
3. **Aggregations:** COUNT, SUM, AVG, GROUP BY, HAVING
4. **NULL behavior** (critical for real data!)
5. **Window functions primer:**
   - ROW_NUMBER() for deduplication
   - LAG() for period-over-period change
   - Moving averages

---

# Learning Objectives

By the end of this block, you'll be able to:

✅ Write SQL queries to filter and sort data
✅ Aggregate data with GROUP BY
✅ Handle NULL values correctly
✅ Use ROW_NUMBER() to select "latest per ID"
✅ Use LAG() to calculate period-over-period changes
✅ Compute moving averages with window frames

---

# The Dataset

**UK Online Retail Data**
- **525,461 transactions** (Dec 2009 – Dec 2010)
- Real-scale data from a gift retailer
- Multiple countries, ~4,000 customers
- Has data quality issues (NULLs, negatives, cancellations)

**This is why SQL + DuckDB matters.**

You could never do this in Excel.

---

# DuckDB: SQL for Data Analysis

**Why DuckDB?**
- SQL database that runs **in-process** (no server!)
- Optimized for **analytics** (not transactions)
- Queries 500K+ rows in milliseconds
- Works directly on CSV/Parquet files
- Perfect for data analysis workflows

**Python API:**
```python
import duckdb
con = duckdb.connect('database.db')
result = con.execute("SELECT ...").df()
```

---

# Window Functions: Mental Model

**Two ways to compute across rows:**

**GROUP BY:** Collapses rows
```sql
SELECT country, COUNT(*)
FROM sales GROUP BY country
-- 38 countries → 38 result rows
```

**Window functions:** Keep rows
```sql
SELECT *, ROW_NUMBER() OVER (PARTITION BY country ORDER BY date)
FROM sales
-- 525K rows → 525K result rows (with row number)
```

**Windows keep row count. GROUP BY reduces it.**

---

# Materials for Today

**Teaching notebooks:**
- `day1_block_b_01_sql_foundations.ipynb`
- `day1_block_b_02_aggregations.ipynb`
- `day1_block_b_03_window_functions.ipynb`

**Quick reference:**
`references/sql_quick_reference.md`

**Homework 1 assigned at end** (due start of Day 2)

---

<!-- _class: lead -->

# Let's Query Some Data

Open the first notebook:
`day1_block_b_01_sql_foundations.ipynb`

We'll start simple and build up to complex queries.
