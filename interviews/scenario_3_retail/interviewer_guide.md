# Scenario 3: Retail Store Operations
## Whiteboard Interview Simulation - Interviewer Guide

**Duration:** 25 minutes
**Difficulty:** Beginner-Intermediate
**Focus:** Store operations, inventory management, regional analysis, NULL awareness

---

## Overview

This scenario simulates a data analyst interview at a multi-location retail chain (think Target, Walmart regional operations, or a boutique chain). Students will analyze store performance, inventory, and transactions across multiple locations. This is the most "traditional" business scenario.

**Key Learning Objectives:**
- Multi-location retail analytics
- LEFT JOIN for finding gaps (inventory vs sales)
- Regional aggregation
- Handling stores with zero activity (NULL awareness)
- Business operational metrics

---

## Pre-Interview Setup (5 minutes before student arrives)

### 1. Load Sample Data on Your Laptop

```bash
cd /Users/earino/CEU/ECBS5294/interviews/scenario_3_retail
```

In Python/Jupyter:
```python
import duckdb
con = duckdb.connect(':memory:')

# Load all tables
con.execute("CREATE TABLE stores AS SELECT * FROM 'data/stores.csv'")
con.execute("CREATE TABLE employees AS SELECT * FROM 'data/employees.csv'")
con.execute("CREATE TABLE transactions AS SELECT * FROM 'data/transactions.csv'")
con.execute("CREATE TABLE inventory AS SELECT * FROM 'data/inventory.csv'")

print("✅ Data loaded successfully!")
```

### 2. Have This Guide Open

Keep this guide visible on your laptop for reference during the interview.

### 3. Prepare Whiteboard

Clear whiteboard, have 2-3 markers ready.

---

## Interview Timeline (25 minutes)

| Time | Activity |
|------|----------|
| 0-2 min | Welcome, scenario setup |
| 2-7 min | Question 1 (stores in CA with high sales) |
| 7-13 min | Question 2 (average transaction by region) |
| 13-19 min | Question 3 (out-of-stock products with recent sales) |
| 19-24 min | Question 4 (data thinking: stores with no transactions) |
| 24-25 min | Wrap-up, feedback |

---

## PART 1: Scenario Introduction (0-2 minutes)

### Script (Read to Student)

> "Welcome! This is a SQL whiteboard interview simulation for a Data Analyst role at **RetailCo**, a regional retail chain with 15 stores across the western United States. RetailCo sells general merchandise—clothing, home goods, electronics, etc.
>
> You're working with the Director of Store Operations, who's preparing a quarterly review. They need insights about store performance, inventory management, and staffing.
>
> You'll work with four tables: `stores`, `employees`, `transactions`, and `inventory`. Let me draw the schema..."

### Draw This Schema on Whiteboard

```
┌─────────────────────────┐
│       stores            │
│─────────────────────────│
│ store_id (VARCHAR)      │ PK
│ store_name (VARCHAR)    │
│ city (VARCHAR)          │
│ state (VARCHAR)         │
│ region (VARCHAR)        │  'West', 'Southwest', 'Northwest'
│ opened_date (DATE)      │
└─────────────────────────┘
           │
           │ 1:many
           │
┌──────────▼──────────────┐
│     employees           │
│─────────────────────────│
│ employee_id (VARCHAR)   │ PK
│ store_id (VARCHAR)      │ FK
│ name (VARCHAR)          │
│ position (VARCHAR)      │  'manager', 'associate', 'cashier'
│ hire_date (DATE)        │
└─────────────────────────┘


┌─────────────────────────┐         ┌─────────────────────────┐
│    transactions         │         │      inventory          │
│─────────────────────────│         │─────────────────────────│
│ transaction_id (VARCHAR)│ PK      │ inventory_id (VARCHAR)  │ PK
│ store_id (VARCHAR)      │ FK      │ store_id (VARCHAR)      │ FK
│ transaction_date (DATE) │         │ product_sku (VARCHAR)   │
│ product_sku (VARCHAR)   │         │ product_name (VARCHAR)  │
│ quantity (INTEGER)      │         │ stock_level (INTEGER)   │  ⚠️ 0 = out of stock
│ amount (DECIMAL)        │         │ last_updated (DATE)     │
└─────────────────────────┘         └─────────────────────────┘
```

### Explain Key Points

- **15 stores** across 3 regions: West, Southwest, Northwest
- **Transactions** are daily sales (one row per item sold)
- **Inventory** tracks current stock levels by SKU and store
- **stock_level = 0** means out of stock
- **Some stores may have zero transactions** in the time period (important for Q4!)
- **Time frame for analysis:** April 2024

**Say to student:** "Any questions about the tables?"

---

## QUESTION 1: Warm-Up (2-7 minutes)

### The Question

> "Let's start with something straightforward. Our regional director wants to know: which California stores had **total sales exceeding $50,000 in April 2024**? Show me the store_name, city, and total sales. Sort by total sales descending."

### What You're Testing
- Basic JOIN (stores + transactions)
- WHERE with date filtering and state comparison
- GROUP BY with SUM aggregation
- HAVING clause for filtering aggregated results
- ORDER BY

### Expected Solution

```sql
SELECT
    s.store_name,
    s.city,
    SUM(t.amount) AS total_sales
FROM stores s
INNER JOIN transactions t ON s.store_id = t.store_id
WHERE s.state = 'CA'
  AND t.transaction_date >= '2024-04-01'
  AND t.transaction_date < '2024-05-01'
GROUP BY s.store_name, s.city
HAVING SUM(t.amount) > 50000
ORDER BY total_sales DESC;
```

**Key points:**
- JOIN stores + transactions
- Filter for California AND April in WHERE
- GROUP BY store (store_name + city)
- HAVING to filter for sales > $50K **after** aggregation
- ORDER BY sales descending

### Alternative Acceptable Solutions

**Using BETWEEN for dates:**
```sql
WHERE s.state = 'CA'
  AND t.transaction_date BETWEEN '2024-04-01' AND '2024-04-30'
```
✅ Acceptable (though < '2024-05-01' is more precise)

**Using table aliases differently (any clear aliases are fine):**
```sql
FROM stores str
JOIN transactions txn ON str.store_id = txn.store_id
```

### Common Mistakes to Watch For

❌ **Mistake 1: Using WHERE instead of HAVING for sales threshold**
```sql
WHERE SUM(t.amount) > 50000  -- Error! Can't use aggregate in WHERE
```
**Probe:** "Can you filter on an aggregated value in WHERE? Where should that go?"

❌ **Mistake 2: Forgetting GROUP BY**
```sql
SELECT s.store_name, SUM(t.amount)
FROM ...
-- Missing GROUP BY s.store_name
```
**Probe:** "What happens when you aggregate without GROUP BY?"

❌ **Mistake 3: Incomplete GROUP BY (missing city)**
```sql
GROUP BY s.store_name  -- If two stores have same name in different cities, this might error
```
**Say:** "Good! Though if store names aren't unique, you might want to include city too. Safer: GROUP BY s.store_name, s.city"

❌ **Mistake 4: Wrong date filtering**
```sql
WHERE MONTH(transaction_date) = 4  -- Works but less clear
```
**Say:** "That works, but explicit date ranges are clearer and work better with indexes."

❌ **Mistake 5: Filtering with = 'CA' before checking quotes**
```sql
WHERE state = CA  -- Missing quotes!
```

### Verification Query (Run on Your Laptop)

```python
student_query = """
[paste their SQL]
"""
result = con.execute(student_query).df()
print(f"Found {len(result)} California stores")
print(result)

# Expected: 2-4 stores with sales ranging from $50K-$150K
```

### Timing Guide

- **Under 3 minutes:** Excellent!
- **3-5 minutes:** Good pace.
- **Over 5 minutes:** Nudge: "Think about JOIN, WHERE, GROUP BY, HAVING."

---

## QUESTION 2: Regional Comparison (7-13 minutes)

### The Question

> "Good! Now let's compare regions. What's the **average transaction amount** by region? Include the region name, total number of transactions, and average amount. Sort by average amount descending."

### What You're Testing
- Multi-table JOIN
- GROUP BY region
- COUNT vs aggregate calculations
- AVG function
- Understanding of aggregation grain

### Expected Solution

```sql
SELECT
    s.region,
    COUNT(t.transaction_id) AS total_transactions,
    ROUND(AVG(t.amount), 2) AS avg_transaction_amount
FROM stores s
INNER JOIN transactions t ON s.store_id = t.store_id
GROUP BY s.region
ORDER BY avg_transaction_amount DESC;
```

**Key points:**
- JOIN stores + transactions to get region
- GROUP BY region (not store!)
- COUNT(transaction_id) counts transactions
- AVG(amount) calculates average per transaction
- ROUND for clean output (optional but nice)

### Alternative Acceptable Solutions

**Without ROUND (perfectly fine):**
```sql
SELECT
    s.region,
    COUNT(*) AS total_transactions,
    AVG(t.amount) AS avg_transaction_amount
FROM stores s
INNER JOIN transactions t ON s.store_id = t.store_id
GROUP BY s.region
ORDER BY avg_transaction_amount DESC;
```

**Adding total sales for context (extra credit):**
```sql
SELECT
    s.region,
    COUNT(*) AS total_transactions,
    ROUND(AVG(t.amount), 2) AS avg_amount,
    ROUND(SUM(t.amount), 2) AS total_sales
FROM stores s
INNER JOIN transactions t ON s.store_id = t.store_id
GROUP BY s.region
ORDER BY avg_amount DESC;
```

### Common Mistakes to Watch For

❌ **Mistake 1: Grouping by store instead of region**
```sql
GROUP BY s.store_id  -- Wrong grain! Want region-level, not store-level
```
**Probe:** "What level are we analyzing? Store or region?"

❌ **Mistake 2: Using SUM instead of AVG**
```sql
SELECT s.region, SUM(t.amount) AS avg_amount  -- That's total, not average!
```
**Probe:** "Is that the total sales or the average per transaction?"

❌ **Mistake 3: Forgetting to JOIN stores table**
```sql
SELECT region, AVG(amount)
FROM transactions
GROUP BY region  -- Error! region isn't in transactions table
```
**Probe:** "Which table has the region column?"

❌ **Mistake 4: Counting stores instead of transactions**
```sql
COUNT(DISTINCT s.store_id) AS total_transactions  -- Counts stores, not transactions!
```
**Probe:** "Are you counting stores or transactions?"

### Follow-Up Probes (Choose 1 if time allows)

**If they finish correctly:**
"What would happen if a store had zero transactions? Would it appear in your results?"
- Expected: "No, INNER JOIN excludes stores with no transactions."

"How would you include stores with zero transactions?"
- Expected: "Use LEFT JOIN from stores to transactions, and COALESCE or handle NULLs."

### Verification Query (Run on Your Laptop)

```python
student_query = """
[paste their SQL]
"""
result = con.execute(student_query).df()
print(result)

# Expected: 3 rows (West, Southwest, Northwest)
# Average amounts should be in range $40-$120
```

### Timing Guide

- **Under 4 minutes:** Great!
- **4-6 minutes:** Good pace.
- **Over 6 minutes:** Nudge: "What table has region? What do you need to GROUP BY?"

---

## QUESTION 3: Inventory Gap Analysis (13-19 minutes)

### The Question

> "Excellent! Now for an operations problem. Our inventory manager needs to restock urgently. Find all products that are **currently out of stock** (stock_level = 0) but **had sales in the past 7 days** (April 8-15, 2024). This means we're losing sales! Show me the product_sku, product_name, store_name, and the date of the last sale. Order by store_name."

### What You're Testing
- LEFT JOIN or INNER JOIN with appropriate logic
- Filtering on stock_level
- Date range filtering
- Understanding of "gap" analysis (inventory vs sales)
- Handling multiple conditions across tables

### Expected Solution

**Approach 1: Using INNER JOIN (simpler)**
```sql
SELECT DISTINCT
    i.product_sku,
    i.product_name,
    s.store_name,
    MAX(t.transaction_date) AS last_sale_date
FROM inventory i
INNER JOIN stores s ON i.store_id = s.store_id
INNER JOIN transactions t ON i.store_id = t.store_id
    AND i.product_sku = t.product_sku
WHERE i.stock_level = 0
  AND t.transaction_date >= '2024-04-08'
  AND t.transaction_date <= '2024-04-15'
GROUP BY i.product_sku, i.product_name, s.store_name
ORDER BY s.store_name;
```

**Key points:**
- Join inventory → stores → transactions
- Match on BOTH store_id AND product_sku between inventory and transactions
- Filter for stock_level = 0 (out of stock now)
- Filter for recent sales (past 7 days)
- MAX(transaction_date) gets the most recent sale

**Approach 2: Using subquery (also valid)**
```sql
SELECT
    i.product_sku,
    i.product_name,
    s.store_name,
    (SELECT MAX(t.transaction_date)
     FROM transactions t
     WHERE t.store_id = i.store_id
       AND t.product_sku = i.product_sku
       AND t.transaction_date >= '2024-04-08'
       AND t.transaction_date <= '2024-04-15') AS last_sale_date
FROM inventory i
INNER JOIN stores s ON i.store_id = s.store_id
WHERE i.stock_level = 0
ORDER BY s.store_name;
```

### Common Mistakes to Watch For

❌ **Mistake 1: Only joining on store_id, forgetting product_sku**
```sql
INNER JOIN transactions t ON i.store_id = t.store_id
-- Missing: AND i.product_sku = t.product_sku
```
**This will return ALL transactions at that store, not just for the out-of-stock product!**
**Probe:** "If you only join on store_id, what transactions will you get?"

❌ **Mistake 2: Not filtering for stock_level = 0**
```sql
-- Shows all inventory, not just out-of-stock items
```
**Probe:** "The question asks for out-of-stock products. How do you identify those?"

❌ **Mistake 3: Wrong date range**
```sql
WHERE transaction_date > '2024-04-07'  -- Close, but includes April 7 too
```
**Minor error—don't penalize heavily. Say:** "Close! Past 7 days from April 15 is April 8-15."

❌ **Mistake 4: Forgetting DISTINCT or GROUP BY**
- If a product sold multiple times in 7 days, it might appear multiple times
**Probe:** "What if this product sold 5 times last week? How many rows would you get?"

### Follow-Up Probes

**If they finish correctly:**
"Great! What would this tell the inventory manager?"
- Expected: "These products are selling well but we're out of stock—we need to reorder immediately."

"What if a product is out of stock but had NO sales in the past 7 days?"
- Expected: "It wouldn't appear in this query. That might mean demand is low, so restocking isn't urgent."

**If they struggle:**
- Prompt: "Which table tells you current stock? Which table tells you past sales? How do you connect them?"

### Verification Query (Run on Your Laptop)

```python
student_query = """
[paste their SQL]
"""
result = con.execute(student_query).df()
print(f"Found {len(result)} out-of-stock products with recent sales")
print(result)

# Expected: 3-6 products
# Check: stock_level should be 0, dates should be April 8-15
```

### Timing Guide

- **Under 5 minutes:** Exceptional! This is tricky.
- **5-7 minutes:** Great pace.
- **Over 7 minutes:** Normal. Nudge: "You need inventory AND transactions. How do they connect?"

---

## QUESTION 4: Data Thinking - Stores with No Activity (19-24 minutes)

This is a discussion question, less about perfect SQL.

### The Question

> "Nice work! Last question: Imagine the Director asks you to create a report showing **total sales by store** for April 2024. You write this query:
>
> ```sql
> SELECT s.store_name, SUM(t.amount) AS total_sales
> FROM stores s
> INNER JOIN transactions t ON s.store_id = t.store_id
> WHERE t.transaction_date >= '2024-04-01'
>   AND t.transaction_date < '2024-05-01'
> GROUP BY s.store_name
> ORDER BY total_sales DESC;
> ```
>
> **Part A:** We have 15 stores, but your query only returns 13 rows. What happened to the other 2 stores?
>
> **Part B:** The Director says, "I need to see ALL 15 stores, even if they had zero sales." How would you modify the query?
>
> **Part C:** If you make that change, what will the total_sales value be for stores with no transactions?"

### What You're Testing
- Understanding of INNER JOIN vs LEFT JOIN
- NULL behavior in aggregations
- Business awareness (all stores should be visible to stakeholders)
- Ability to modify queries based on business requirements
- Understanding of COALESCE or IFNULL for NULL handling

### Expected Answers

**Part A: What happened?**

Good answers:
- ✅ "INNER JOIN only returns rows where there's a match in BOTH tables. The 2 stores had no transactions, so they were excluded."
- ✅ "The missing stores had zero sales in April, so the INNER JOIN dropped them."
- ✅ "INNER JOIN filtered them out because they don't have matching rows in the transactions table."

Red flags:
- ❌ "The data is wrong" - no exploration of JOIN logic
- ❌ "I don't know" - encourage them to reason through it

**Part B: How to fix it?**

Good answers:
- ✅ "Change INNER JOIN to LEFT JOIN so all stores are kept."
```sql
FROM stores s
LEFT JOIN transactions t ON s.store_id = t.store_id
```
- ✅ "Use LEFT JOIN to keep all stores, even without transactions."

Great answer (goes further):
```sql
SELECT
    s.store_name,
    COALESCE(SUM(t.amount), 0) AS total_sales
FROM stores s
LEFT JOIN transactions t ON s.store_id = t.store_id
WHERE t.transaction_date >= '2024-04-01'
      AND t.transaction_date < '2024-05-01'
   OR t.transaction_date IS NULL
GROUP BY s.store_name
ORDER BY total_sales DESC;
```
✅ **Bonus points for COALESCE!**

**Part C: What will total_sales be for stores with no transactions?**

Good answers:
- ✅ "NULL, because SUM of no rows returns NULL."
- ✅ "NULL. That's why we'd use COALESCE(SUM(t.amount), 0) to show 0 instead."

Red flags:
- ❌ "Zero" - technically wrong without COALESCE
- ❌ "Empty" - not precise

**Excellent follow-up if they mention COALESCE:**
"Great! Show me what that looks like."
```sql
SELECT
    s.store_name,
    COALESCE(SUM(t.amount), 0) AS total_sales
FROM stores s
LEFT JOIN transactions t ON s.store_id = t.store_id
GROUP BY s.store_name;
```

### Follow-Up Probes (Choose Based on Their Answer)

**If they mention LEFT JOIN:**
"Excellent! Why is LEFT JOIN better than INNER JOIN here?"
- Expected: "LEFT JOIN keeps all stores, which is what the stakeholder needs."

**If they mention COALESCE:**
"Perfect! What does COALESCE do?"
- Expected: "It replaces NULL with 0, so the report shows $0 instead of NULL for stores with no sales."

**If they struggle:**
- Prompt: "Think about what INNER JOIN requires. What if one table has a row that doesn't match anything in the other table?"

### This is a Discussion - Be Flexible!

- Let them think through the logic
- This tests JOIN understanding more than syntax
- Look for: awareness, reasoning, ability to adapt

---

## SCORING RUBRIC

Use this to evaluate overall performance.

### Technical Correctness (40 points)

| Question | Points | Criteria |
|----------|--------|----------|
| Q1 | 10 pts | Correct JOIN, WHERE, GROUP BY, HAVING, date filtering |
| Q2 | 10 pts | Correct JOIN, GROUP BY region, AVG calculation |
| Q3 | 12 pts | Correct multi-table JOIN with dual keys (store+SKU), filtering, date range |
| Q4 | 8 pts | Understanding of INNER vs LEFT JOIN, NULL behavior |

**Deductions:**
- Syntax errors: -2 pts per query
- Wrong logic but shows understanding: -1 to -2 pts
- Critical conceptual error (e.g., wrong JOIN type): -3 pts

### SQL Best Practices (20 points)

- **Readability (8 pts):** Formatting, clear aliases, logical structure
- **Efficiency awareness (6 pts):** WHERE before HAVING, appropriate JOINs
- **NULL handling (6 pts):** Mentions COALESCE, aware of NULL in aggregations

### Communication & Process (25 points)

- **Thinking out loud (10 pts):** Explains approach
- **Asks clarifying questions (8 pts):** Confirms understanding
- **Handles feedback (7 pts):** Responds to probes

### Data & Business Thinking (15 points)

- **Business context (8 pts):** Understands operational metrics (sales, inventory, out-of-stock urgency)
- **Edge case awareness (7 pts):** Considers stores with no transactions, NULL values

### Total: 100 points

**Scoring bands:**
- **85-100:** Exceptional
- **70-84:** Strong
- **55-69:** Competent
- **Below 55:** Needs review

---

## POST-INTERVIEW: Providing Feedback

### What to Say

**If they did well (70+):**
> "Strong work! Your understanding of [JOINs / HAVING clause / inventory analysis] was solid. I especially liked [specific thing]. One area to keep refining: [pick 1]. You're interview-ready!"

**If they struggled (55-69):**
> "You've got the fundamentals. I'd recommend practicing [multi-table JOINs / HAVING vs WHERE / LEFT JOIN patterns]. Your [positive note] was good. Keep practicing!"

**If they really struggled (<55):**
> "You understand the basics, which is great. Before interviews, focus on [specific topics]. Come to office hours if you'd like to walk through these together. Practicing now will pay off!"

### Always End Positively

- "These simulations are challenging—great job coming in!"
- "Every practice round makes you stronger!"
- "You're building valuable skills. Keep it up!"

---

## QUICK REFERENCE: Key Concepts

### Critical Patterns
- ✅ HAVING for filtering aggregated results (not WHERE)
- ✅ LEFT JOIN to include all stores (even with zero activity)
- ✅ Joining on multiple keys (store_id AND product_sku)
- ✅ COALESCE for NULL replacement

### Green Flags
- Asks about date ranges
- Mentions HAVING vs WHERE distinction
- Considers stores with no transactions
- Uses COALESCE for NULL handling

### Red Flags
- Uses WHERE for aggregate filtering
- Forgets to join on both store_id and product_sku (Q3)
- Doesn't understand INNER vs LEFT JOIN difference
- Silent—doesn't explain thinking

---

## APPENDIX: Quick Verification Queries

### Check: CA stores with sales > $50K
```python
con.execute("""
    SELECT s.store_name, SUM(t.amount) AS sales
    FROM stores s
    JOIN transactions t ON s.store_id = t.store_id
    WHERE s.state = 'CA'
      AND t.transaction_date >= '2024-04-01'
      AND t.transaction_date < '2024-05-01'
    GROUP BY s.store_name
    HAVING SUM(t.amount) > 50000
""").df()
```

### Check: Average transaction by region
```python
con.execute("""
    SELECT s.region, AVG(t.amount) AS avg_amount
    FROM stores s
    JOIN transactions t ON s.store_id = t.store_id
    GROUP BY s.region
""").df()
```

### Check: Out-of-stock with recent sales
```python
con.execute("""
    SELECT i.product_sku, i.product_name, s.store_name
    FROM inventory i
    JOIN stores s ON i.store_id = s.store_id
    JOIN transactions t ON i.store_id = t.store_id AND i.product_sku = t.product_sku
    WHERE i.stock_level = 0
      AND t.transaction_date >= '2024-04-08'
""").df()
```

---

## End of Interviewer Guide

**Remember:** This scenario tests operational/business thinking. Focus on whether they understand the *why* behind the queries, not just the syntax.

Good luck with the interviews! 🎯
