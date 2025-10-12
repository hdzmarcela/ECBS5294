---
marp: true
theme: ceu
paginate: true
header: 'Day 2, Block B: APIs & JSON Normalization'
footer: 'ECBS5294 | CEU'
---

<!-- _class: lead -->

# Block B
## REST APIs & JSON to DuckDB

**90 minutes**

---

# What We'll Cover

1. **REST API fundamentals** (GET requests, status codes, JSON)
2. **JSON structure** (objects, arrays, nesting)
3. **Safe navigation** (`.get()` pattern for missing fields)
4. **Normalization** (nested JSON → relational tables)
5. **One-to-many relationships** (products → reviews)
6. **Persisting to DuckDB** (for SQL analysis)
7. **Complete pipeline:** API → Parse → Normalize → DuckDB → SQL

---

# Learning Objectives

By the end of this block, you'll be able to:

✅ Fetch data from REST APIs using Python `requests`
✅ Navigate nested JSON structures safely
✅ Handle missing fields without crashing pipelines
✅ Normalize one-to-many relationships into separate tables
✅ Persist JSON data to DuckDB tables
✅ Join normalized tables to answer business questions

---

# The Real-World Scenario

**Your boss:**
> "We need a dashboard showing product ratings and review volume. Pull the data from our e-commerce API."

**Your challenge:**
1. Fetch product data from API (returns JSON)
2. Extract nested reviews (one product → many reviews)
3. Create two tables: `products` and `reviews`
4. Load into DuckDB
5. Write SQL to analyze ratings

**This is the modern data pipeline.**

---

# Why APIs Matter

**Modern business data lives in APIs:**
- **Stripe:** Payment transactions
- **Shopify:** Orders, inventory, customers
- **Salesforce:** CRM data
- **Google Analytics:** Website traffic
- **Twitter/LinkedIn:** Social media data

**If you can't ingest from APIs, you can't build data pipelines.**

---

# The JSON Challenge

**APIs return JSON. JSON is nested.**

```json
{
  "product": {
    "id": 1,
    "title": "Widget",
    "reviews": [
      {"rating": 5, "comment": "Great!"},
      {"rating": 4, "comment": "Good"}
    ]
  }
}
```

**Problem:** SQL doesn't work on nested structures.
**Solution:** Normalize to flat tables.

---

# Normalization: The Pattern

### Before: Nested JSON (Can't query with SQL ❌)

```json
{
  "products": [
    {
      "id": 1,
      "title": "Widget",
      "reviews": [
        {"rating": 5, "comment": "Great!"},
        {"rating": 4, "comment": "Good"}
      ]
    }
  ]
}
```

**Problem:** How do you query "average rating per product" in nested JSON? You can't!

---

# Normalization: The Pattern

### After: Relational Tables (SQL-ready ✅)

**`products` table:**
| product_id | title  |
|------------|--------|
| 1          | Widget |
| 2          | Gadget |

**`reviews` table:**
| review_id | product_id | rating | comment |
|-----------|------------|--------|---------|
| 1         | 1          | 5      | Great!  |
| 2         | 1          | 4      | Good    |
| 3         | 2          | 5      | Love it |

**Now you can query:**
```sql
SELECT p.title, AVG(r.rating) as avg_rating
FROM products p
LEFT JOIN reviews r ON p.product_id = r.product_id
GROUP BY p.title
```

---

# The Two Notebooks

### Notebook 1: API & JSON Basics (30 min)
- Fetching data from DummyJSON API
- Navigating JSON structures
- Safe access with `.get()`
- Common mistakes and how to avoid them

### Notebook 2: JSON to DuckDB (60 min)
- Normalizing nested reviews
- Creating relational tables
- Persisting to DuckDB
- Joining tables for analysis
- Complete end-to-end pipeline

---

# Key Insight

> **"Every modern data pipeline starts with API ingestion. Master this, and you can pull data from anywhere."**

- Static CSV files: **Good for learning**
- Live APIs: **How production pipelines work**

**Today you build your first production-ready data pipeline.**

---

# Materials for Today

**Teaching notebooks:**
- `day2_block_b_01_api_json_basics.ipynb`
- `day2_block_b_02_json_to_duckdb.ipynb`

**API endpoint:**
DummyJSON (no auth required, free, reliable)

**Quick reference:**
`references/api_pipeline_quick_reference.md`

**Homework 2 assigned at end** (due start of Day 3)

---

<!-- _class: lead -->

# Let's Fetch Some Data

Open the first notebook:
`day2_block_b_01_api_json_basics.ipynb`

We'll make our first API request and explore the JSON structure.

---
