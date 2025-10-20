# Day 3 Datasets

This directory contains datasets for Day 3 teaching and assignments.

---

## Overview

**Day 3 Focus:** Data pipelines, validations, and real-world data integration

---

## Directory Structure

```
day3/
├── teaching/          # Day 3 Block A teaching materials
├── exercise/          # Day 3 in-class exercise
└── hw3_data_pack/     # HW3 assignment datasets
```

---

## Teaching Data (Block A)

**Location:** `teaching/`
**Used in:** `notebooks/day3/day3_block_a_pipelines_and_validations.ipynb`

### Files

- `olist_orders_subset.csv` (1,000 orders)
- `olist_customers_subset.csv` (1,000 customers)
- `olist_order_items_subset.csv` (~1,100 order items)

### Description

Subset of the Brazilian E-Commerce (Olist) dataset used in Day 2. This familiar data allows students to focus on pipeline patterns and validation techniques without learning a new domain.

**Why reuse Olist?**
- Students already understand the business context
- Known schema (no time spent on "what is this field?")
- Focus on **how** to build pipelines, not **what** the data means
- Demonstrates real-world pattern: iterative work with same data sources

**Source:** Kaggle - Brazilian E-Commerce Public Dataset by Olist
**Original License:** CC BY-NC-SA 4.0
**Size:** Randomly sampled 1,000 orders (1% of full dataset)
**Random Seed:** 42 (reproducible sampling)

---

## Exercise Data (In-Class)

**Location:** `exercise/`
**Used in:** `notebooks/day3/day3_exercise_mini_pipeline.ipynb`

### Files

- `mini_orders.csv` (500 orders)
- `mini_customers.csv` (500 customers)
- `mini_order_items.csv` (~540 order items)

### Description

Smaller subset of Olist data for in-class 15-minute exercise. Students build a 3-stage pipeline (bronze → silver → gold) with validations.

**Source:** Same as teaching data (different random sample)
**Size:** 500 orders (0.5% of full dataset)
**Random Seed:** 123 (different from teaching data)
**Time Limit:** 15 minutes
**Grading:** Completion-based (5% of course grade)

---

## HW3 Data Pack

**Location:** `hw3_data_pack/`
**Used in:** `assignments/hw3/`

### Files

- `chicago_business_licenses.csv` (50,000 licenses)
- `nyc_building_permits.json` (20,000 permits)
- `README.md` (comprehensive attribution & documentation)

### Description

Real government data from Chicago and NYC open data portals. Multi-format, multi-source integration project testing all skills from Days 1-3.

**Formats:**
- CSV (structured relational)
- JSON (requires parsing and normalization)

**Source:** City of Chicago Data Portal + NYC Open Data
**License:** Public Domain (U.S. Government Work)
**Size:** ~70,000 total records, ~50MB total
**Natural Messiness:** Real-world data quality issues (no artificial corruption)

**See:** `hw3_data_pack/README.md` for complete documentation

---

## Data Preparation

All Day 3 datasets were created using:
```bash
python scripts/prepare_day3_datasets.py
```

This script:
1. Samples Olist data for teaching and exercise
2. Downloads Chicago business licenses (CSV)
3. Downloads NYC building permits (JSON)
4. Saves all files with proper attribution

---

## Attribution

### Olist Data (Teaching & Exercise)
**Source:** Kaggle - Brazilian E-Commerce Public Dataset by Olist
**URL:** https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
**License:** CC BY-NC-SA 4.0
**Usage:** Educational use permitted with attribution

**Attribution:**
> Brazilian E-Commerce Public Dataset by Olist. (2018). Retrieved from https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce. Licensed under CC BY-NC-SA 4.0.

### Chicago & NYC Data (HW3)
**Sources:**
- City of Chicago Data Portal (data.cityofchicago.org)
- NYC Open Data (data.cityofnewyork.us)

**License:** Public Domain (U.S. Government Work)
**Usage:** No restrictions

**Full attribution:** See `hw3_data_pack/README.md`

---

## Using This Data

### Load Teaching Data
```python
import duckdb

con = duckdb.connect(':memory:')

# Load teaching subset
con.execute("CREATE TABLE orders AS SELECT * FROM 'data/day3/teaching/olist_orders_subset.csv'")
con.execute("CREATE TABLE customers AS SELECT * FROM 'data/day3/teaching/olist_customers_subset.csv'")
con.execute("CREATE TABLE order_items AS SELECT * FROM 'data/day3/teaching/olist_order_items_subset.csv'")

# Verify
result = con.execute("SELECT COUNT(*) FROM orders").fetchone()
print(f"Loaded {result[0]} orders")
```

### Load Exercise Data
```python
# Load mini subset
con.execute("CREATE TABLE mini_orders AS SELECT * FROM 'data/day3/exercise/mini_orders.csv'")
con.execute("CREATE TABLE mini_customers AS SELECT * FROM 'data/day3/exercise/mini_customers.csv'")
con.execute("CREATE TABLE mini_items AS SELECT * FROM 'data/day3/exercise/mini_order_items.csv'")
```

### Load HW3 Data
See `hw3_data_pack/README.md` for detailed instructions on loading multi-format data.

---

## Notes

- All paths are relative to repository root
- All notebooks use relative paths (no absolute paths!)
- Data is offline (no API calls required)
- Restart & Run All should work on any machine

---

**Questions?** See individual README files in each subdirectory for more details.
