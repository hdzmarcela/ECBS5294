# Recommended Kaggle Datasets for Teaching Data Cleaning

## 1. Cafe Sales - Dirty Data for Cleaning Training

**Source:** https://www.kaggle.com/datasets/ahmedmohamed2003/cafe-sales-dirty-data-for-cleaning-training

**Size:** 10,000 rows

**Domain:** Cafe/restaurant transactions (familiar to students)

**Messy Characteristics:**
- Missing values in Item, Payment Method, Location
- Invalid entries like "ERROR" or "UNKNOWN"
- Inconsistent data types (numeric columns with text)
- Date format issues

**Columns:** Transaction ID, Item, Quantity, Price, Payment Method, Date

**Why Good for Block 1:**
- Manageable size for 90-minute session
- Business context students understand (cafe transactions)
- Clear examples of common real-world problems
- Not too overwhelming for absolute beginners

**Teaching Opportunities:**
- Identifying missing values (different representations)
- Type validation (price should be numeric)
- Date parsing
- Creating derived features
- Designating primary keys (Transaction ID)

---

## 2. Retail Store Sales - Dirty for Data Cleaning

**Source:** https://www.kaggle.com/datasets/ahmedmohamed2003/retail-store-sales-dirty-for-data-cleaning

**Size:** 12,575 rows

**Domain:** Retail transactions

**Messy Characteristics:**
- Missing values in Item, Price Per Unit, Quantity
- Invalid entries in Payment Method and Location
- "None" values scattered throughout
- Inconsistent formatting

**Columns:** Customer ID, Item, Price Per Unit, Quantity, Payment Method, Location, Transaction Date

**Why Good for Teaching:**
- 8 product categories, 25 items per category (realistic variety)
- Explicitly designed to "simulate real-world sales data"
- Updated January 2025 (recent)
- Good for showing impact of missing data on aggregations

**Teaching Opportunities:**
- NULL handling in calculations (revenue = price * quantity)
- Grouping with missing categories
- Customer-level analysis with incomplete data
- Primary vs foreign keys (Customer ID as FK)

---

## 3. Other Options Found

- **Dirty Dataset to practice Data Cleaning** - Music tours dataset
- **Messy Food Waste Prediction Dataset** - Competition-style dataset

---

## Recommendation for Day 1 Block A

**Use:** **Cafe Sales Dataset** (10,000 rows)

**Rationale:**
1. Smaller and more manageable for first exposure
2. Single business entity (transactions) - simpler conceptual model
3. Familiar domain (everyone understands cafe purchases)
4. Clear transaction grain (each row = one transaction)
5. Natural primary key (Transaction ID)
6. Good variety of problems without being overwhelming

**Alternative:** Create our own smaller (200-500 row) version by sampling from this dataset and adding specific teaching examples (e.g., dates in multiple formats, currency symbols in prices, etc.)
