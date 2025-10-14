# Scenario 1: E-Commerce Analytics
## Whiteboard Interview Simulation - Interviewer Guide

**Duration:** 25 minutes
**Difficulty:** Beginner-Intermediate
**Focus:** Basic SQL, JOINs, NULL handling, business thinking

---

## Overview

This scenario simulates a data analyst interview at an e-commerce marketplace. Students will write SQL queries on a whiteboard without a computer. This guide provides everything you need to conduct a realistic, structured interview.

**Key Learning Objectives:**
- Basic SELECT/WHERE filtering
- JOIN operations (INNER and LEFT)
- GROUP BY aggregations
- NULL handling awareness
- Business/data quality thinking

---

## Pre-Interview Setup (5 minutes before student arrives)

### 1. Load Sample Data on Your Laptop

```bash
cd /Users/earino/CEU/ECBS5294/interviews/scenario_1_ecommerce
```

In Python/Jupyter:
```python
import duckdb
con = duckdb.connect(':memory:')

# Load all tables
con.execute("CREATE TABLE customers AS SELECT * FROM 'data/customers.csv'")
con.execute("CREATE TABLE orders AS SELECT * FROM 'data/orders.csv'")
con.execute("CREATE TABLE order_items AS SELECT * FROM 'data/order_items.csv'")
con.execute("CREATE TABLE products AS SELECT * FROM 'data/products.csv'")

print("✅ Data loaded successfully!")
```

### 2. Have This Guide Open

Keep this guide visible on your laptop for reference during the interview.

### 3. Prepare Whiteboard

Clear whiteboard, have 2-3 markers ready (black/blue for student, red for corrections if needed).

---

## Interview Timeline (25 minutes)

| Time | Activity |
|------|----------|
| 0-2 min | Welcome, scenario setup |
| 2-7 min | Question 1 (warm-up) |
| 7-13 min | Question 2 (JOIN + aggregation) |
| 13-19 min | Question 3 (LEFT JOIN anti-pattern) |
| 19-24 min | Question 4 (data thinking discussion) |
| 24-25 min | Wrap-up, feedback |

---

## PART 1: Scenario Introduction (0-2 minutes)

### Script (Read to Student)

> "Welcome! Thanks for coming in today. This is a SQL whiteboard interview simulation—it's designed to mimic what you'd experience at companies like Meta, Amazon, or other tech companies when interviewing for data analyst or analytics engineer roles.
>
> Here's how this works: I'm going to describe a business scenario and some database tables. You'll write SQL queries on the whiteboard to answer business questions. Feel free to think out loud—I want to hear your thought process. You can ask clarifying questions at any time. Ready?
>
> **The Scenario:**
> You're interviewing for a Data Analyst role at **ShopFast**, an online marketplace similar to Amazon or Olist. The company has customers who place orders, and each order can contain multiple items from different product categories.
>
> You'll be working with four tables: `customers`, `orders`, `order_items`, and `products`. Let me draw the schema for you..."

### Draw This Schema on Whiteboard

```
┌─────────────────────────┐
│      customers          │
│─────────────────────────│
│ customer_id (VARCHAR)   │ PK
│ customer_city (VARCHAR) │
│ customer_state (VARCHAR)│  ⚠️ ~10% are NULL
│ created_date (DATE)     │
└─────────────────────────┘
           │
           │ 1:many
           │
┌──────────▼──────────────┐
│       orders            │
│─────────────────────────│
│ order_id (VARCHAR)      │ PK
│ customer_id (VARCHAR)   │ FK
│ order_date (DATE)       │
│ order_status (VARCHAR)  │  'delivered', 'canceled', 'processing'
│ total_amount (DECIMAL)  │
└─────────────────────────┘
           │
           │ 1:many
           │
┌──────────▼──────────────┐         ┌─────────────────────────┐
│     order_items         │         │       products          │
│─────────────────────────│         │─────────────────────────│
│ order_id (VARCHAR)      │ FK      │ product_id (VARCHAR)    │ PK
│ product_id (VARCHAR)    │ FK ────▶│ product_name (VARCHAR)  │
│ quantity (INTEGER)      │         │ category (VARCHAR)      │
│ price (DECIMAL)         │         └─────────────────────────┘
└─────────────────────────┘
```

### Explain Key Points

- **IDs are strings** (VARCHAR), not integers - hash-based IDs like "a1b2c3..."
- **One customer can have many orders** (1:many relationship)
- **One order can have many items** (1:many relationship)
- **customer_state has ~10% NULL values** (important for later!)
- **order_status** can be 'delivered', 'canceled', or 'processing'

**Say to student:** "Any questions about the tables before we start?"

---

## QUESTION 1: Warm-Up (2-7 minutes)

### The Question

> "Let's start with something basic to warm up. Show me all delivered orders from March 2024 where the total amount was greater than $100. Return the order_id, order_date, and total_amount. Sort by total_amount descending."

### What You're Testing
- Basic SELECT syntax
- WHERE clause with multiple conditions (AND)
- Date filtering
- Comparison operators
- ORDER BY

### Expected Solution

```sql
SELECT
    order_id,
    order_date,
    total_amount
FROM orders
WHERE order_status = 'delivered'
  AND order_date >= '2024-03-01'
  AND order_date < '2024-04-01'
  AND total_amount > 100
ORDER BY total_amount DESC;
```

**Alternative acceptable solutions:**
- Using `BETWEEN` for dates: `order_date BETWEEN '2024-03-01' AND '2024-03-31'` ✅
- Using `DATE_TRUNC` or similar: `DATE_TRUNC('month', order_date) = '2024-03-01'` ✅
- Single quotes vs double quotes around dates (both work) ✅

### Common Mistakes to Watch For

❌ **Mistake 1: Missing quotes around 'delivered'**
```sql
WHERE order_status = delivered  -- WRONG! Needs quotes
```
**Probe:** "Is 'delivered' a column name or a string value?"

❌ **Mistake 2: Incorrect date comparison**
```sql
WHERE order_date = '2024-03'  -- WRONG! Need full date or range
```
**Probe:** "How would you select all dates in March?"

❌ **Mistake 3: Using OR instead of AND**
```sql
WHERE order_status = 'delivered' OR total_amount > 100  -- WRONG logic!
```
**Probe:** "Do you want orders that are delivered OR expensive, or orders that are BOTH?"

❌ **Mistake 4: Forgetting ORDER BY**
- If they forget, ask: "How will the results be ordered?"

### Verification Query (Run on Your Laptop)

Copy their SQL exactly as written and run it:

```python
# Their query here
student_query = """
[paste their SQL]
"""
result = con.execute(student_query).df()
print(f"Returned {len(result)} rows")
print(result.head())

# Expected: ~8-12 rows with order dates in March 2024
```

### Timing Guide

- **Under 3 minutes:** Excellent! Move on quickly.
- **3-5 minutes:** Good pace, normal.
- **Over 5 minutes:** Gently nudge if stuck: "What parts of the WHERE clause do you need?"

---

## QUESTION 2: Core Skills - JOIN + Aggregation (7-13 minutes)

### The Question

> "Good! Now let's step it up. Our VP wants to know: **What's the total revenue by product category for delivered orders?** Show me the category name, total revenue, and number of orders. Sort by total revenue descending."

### What You're Testing
- INNER JOIN across multiple tables
- Understanding of many-to-many relationships (orders → order_items → products)
- GROUP BY with aggregation
- COUNT vs COUNT(DISTINCT)
- Aliasing calculated columns

### Expected Solution

```sql
SELECT
    p.category,
    COUNT(DISTINCT oi.order_id) AS num_orders,
    SUM(oi.price * oi.quantity) AS total_revenue
FROM order_items oi
INNER JOIN products p ON oi.product_id = p.product_id
INNER JOIN orders o ON oi.order_id = o.order_id
WHERE o.order_status = 'delivered'
GROUP BY p.category
ORDER BY total_revenue DESC;
```

**Key points:**
- Need to join THREE tables: order_items → products → orders
- Must filter for `order_status = 'delivered'` (in orders table)
- Use `COUNT(DISTINCT oi.order_id)` not `COUNT(*)` to avoid duplicate inflation
- Calculate revenue as `price * quantity`

### Alternative Acceptable Solutions

**Option 1: Different join order (equally valid)**
```sql
SELECT
    p.category,
    COUNT(DISTINCT o.order_id) AS num_orders,
    SUM(oi.price * oi.quantity) AS total_revenue
FROM orders o
INNER JOIN order_items oi ON o.order_id = oi.order_id
INNER JOIN products p ON oi.product_id = p.product_id
WHERE o.order_status = 'delivered'
GROUP BY p.category
ORDER BY total_revenue DESC;
```

**Option 2: Using table aliases consistently** (any reasonable aliases are fine)

### Common Mistakes to Watch For

❌ **Mistake 1: Only joining 2 tables (forgetting orders table for status filter)**
```sql
-- Missing orders table!
SELECT p.category, SUM(oi.price * oi.quantity) AS revenue
FROM order_items oi
INNER JOIN products p ON oi.product_id = p.product_id
GROUP BY p.category
```
**Probe:** "How will you filter for delivered orders if you don't join the orders table?"

❌ **Mistake 2: Using COUNT(*) instead of COUNT(DISTINCT order_id)**
```sql
SELECT p.category, COUNT(*) AS num_orders  -- WRONG! Counts items, not orders
```
**Probe:** "If an order has 3 items in the same category, how many times will it be counted?"

❌ **Mistake 3: Forgetting to multiply price * quantity**
```sql
SELECT p.category, SUM(oi.price) AS total_revenue  -- Missing quantity!
```
**Probe:** "If someone orders 5 units at $10 each, what should the revenue be?"

❌ **Mistake 4: Incorrect GROUP BY (missing category or grouping by wrong columns)**
```sql
GROUP BY product_id  -- WRONG! Should group by category
```

❌ **Mistake 5: Filtering with HAVING instead of WHERE for order_status**
```sql
-- Less efficient but technically works
WHERE ...
GROUP BY p.category
HAVING o.order_status = 'delivered'  -- Can work but WHERE is better
```
**Note:** This might error depending on implementation, but even if it works, it's inefficient. WHERE filters before aggregation (better).

### Follow-Up Probes (Choose 1-2 Based on Time)

**If they finish quickly and correctly:**
1. "What would happen if you used LEFT JOIN instead of INNER JOIN between order_items and products?"
   - Expected: "We might get items with NULL category if a product was deleted."

2. "How would the result change if you removed the WHERE clause filtering for 'delivered'?"
   - Expected: "We'd include canceled and processing orders, inflating revenue."

**If they struggled:**
1. "Walk me through which tables you need and why."
2. "Why did you choose COUNT(*) vs COUNT(DISTINCT)?"

### Verification Query (Run on Your Laptop)

```python
student_query = """
[paste their SQL]
"""
result = con.execute(student_query).df()
print(f"Returned {len(result)} rows")
print(result)

# Expected output: ~5-8 categories with revenue ranging from hundreds to thousands
# Check: Does revenue look reasonable? Are categories present?
```

### Timing Guide

- **Under 4 minutes:** Excellent! Strong candidate.
- **4-6 minutes:** Good pace.
- **Over 6 minutes:** This is the hardest question—nudge if needed: "What tables do you need to answer this?"

---

## QUESTION 3: LEFT JOIN Anti-Pattern (13-19 minutes)

### The Question

> "Nice work! Here's a business problem: Our customer success team wants to follow up with customers in California who **placed orders in March 2024 but haven't ordered anything in April 2024**. Write a query to find these customers. Return the customer_id and customer_city."

### What You're Testing
- LEFT JOIN conceptual understanding
- Anti-join pattern (finding non-matches)
- Date filtering across two time periods
- IS NULL for detecting missing matches
- More complex business logic

### Expected Solution (Multiple Valid Approaches)

**Approach 1: LEFT JOIN with anti-join pattern**
```sql
SELECT DISTINCT
    c.customer_id,
    c.customer_city
FROM customers c
INNER JOIN orders o_march ON c.customer_id = o_march.customer_id
LEFT JOIN orders o_april ON c.customer_id = o_april.customer_id
    AND o_april.order_date >= '2024-04-01'
    AND o_april.order_date < '2024-05-01'
WHERE c.customer_state = 'CA'
  AND o_march.order_date >= '2024-03-01'
  AND o_march.order_date < '2024-04-01'
  AND o_april.order_id IS NULL;
```

**Approach 2: NOT IN subquery**
```sql
SELECT DISTINCT
    c.customer_id,
    c.customer_city
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
WHERE c.customer_state = 'CA'
  AND o.order_date >= '2024-03-01'
  AND o.order_date < '2024-04-01'
  AND c.customer_id NOT IN (
      SELECT customer_id
      FROM orders
      WHERE order_date >= '2024-04-01'
        AND order_date < '2024-05-01'
  );
```

**Approach 3: NOT EXISTS subquery**
```sql
SELECT DISTINCT
    c.customer_id,
    c.customer_city
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
WHERE c.customer_state = 'CA'
  AND o.order_date >= '2024-03-01'
  AND o.order_date < '2024-04-01'
  AND NOT EXISTS (
      SELECT 1
      FROM orders o2
      WHERE o2.customer_id = c.customer_id
        AND o2.order_date >= '2024-04-01'
        AND o2.order_date < '2024-05-01'
  );
```

**All three approaches are correct!** The LEFT JOIN approach tests their understanding from class most directly.

### Common Mistakes to Watch For

❌ **Mistake 1: Using = NULL instead of IS NULL**
```sql
LEFT JOIN ...
WHERE o_april.order_id = NULL  -- WRONG! Use IS NULL
```
**Critical probe:** "How do you check for NULL values in SQL?"

❌ **Mistake 2: Forgetting DISTINCT**
- If customer placed multiple orders in March, they'll appear multiple times
**Probe:** "If a customer placed 3 orders in March, how many times will they appear in your result?"

❌ **Mistake 3: Wrong date filtering logic**
```sql
-- Including both months instead of separating them
WHERE o.order_date >= '2024-03-01' AND o.order_date < '2024-05-01'
```
**Probe:** "This gets orders from March OR April. How do we find customers who ordered in March but NOT April?"

❌ **Mistake 4: Forgetting to filter for California (customer_state = 'CA')**

❌ **Mistake 5: Using INNER JOIN for April instead of LEFT JOIN**
- This would only return customers who ordered in BOTH months (opposite of what we want!)

### Follow-Up Probes

**If they finish correctly:**
"Walk me through why you used LEFT JOIN for April orders but INNER JOIN for March orders."
- Expected: "INNER JOIN for March ensures they ordered in March. LEFT JOIN for April lets us find NULL (no orders in April)."

**If they used NOT IN or NOT EXISTS:**
"That's a valid approach! How would you solve this with a LEFT JOIN instead?"

### Verification Query (Run on Your Laptop)

```python
student_query = """
[paste their SQL]
"""
result = con.execute(student_query).df()
print(f"Found {len(result)} customers")
print(result.head(10))

# Expected: 5-15 customers
# Sanity check: All should have customer_state = 'CA'
```

### Timing Guide

- **Under 5 minutes:** Exceptional! This is hard.
- **5-7 minutes:** Great pace.
- **Over 7 minutes:** Totally normal for this complexity. Nudge: "Think about what LEFT JOIN gives you when there's no match."

---

## QUESTION 4: Data Thinking & Business Logic (19-24 minutes)

This is less about perfect SQL and more about **how they think about data**. It's a discussion question.

### The Question

> "Great! Let's talk about data quality. I mentioned earlier that about 10% of customers have NULL for their customer_state.
>
> **Part A:** How would your query from Question 3 behave if a California customer's state value was actually NULL instead of 'CA'?
>
> **Part B:** If you were asked to report 'total revenue by customer state' and 10% of states are NULL, how would you handle that in your analysis? What would you tell the stakeholder?"

### What You're Testing
- Understanding of NULL behavior in WHERE clauses
- Data quality awareness
- Business communication skills
- Ability to make reasonable assumptions
- Awareness of edge cases

### Expected Answers

**Part A: Technical Understanding**

Good answers include:
- ✅ "The customer would be **excluded** from the results because `WHERE customer_state = 'CA'` doesn't match NULL."
- ✅ "NULL is not equal to anything, including 'CA', so the WHERE clause filters them out."
- ✅ "We'd miss them. If we wanted to include customers with NULL state, we'd need to add `OR customer_state IS NULL`."

Red flags:
- ❌ "NULL equals 'CA'" - fundamentally misunderstands NULL
- ❌ "NULL would match 'CA'" - no!
- ❌ "I'm not sure" - encourage them to reason through it

**Part B: Business Communication**

Good answers include:
- ✅ "I'd create a separate category for NULL states, maybe labeled 'Unknown' or 'Missing', so stakeholders see it explicitly."
- ✅ "I'd report the NULL values separately and document in my analysis that 10% of revenue has unknown location."
- ✅ "I'd investigate WHY states are NULL—is it a data collection issue? New customers? Then decide how to categorize them."
- ✅ "I'd ask the stakeholder if they want to see 'Unknown' as its own category or exclude it from the report. Depends on the business question."

Great answers go further:
- ✅ "I'd check if NULL states correlate with other factors—maybe they're all international orders or test accounts."
- ✅ "I'd use `COALESCE(customer_state, 'Unknown')` to make NULLs explicit in the report."
- ✅ "I'd mention it in the assumptions section of my analysis and note potential impact on decision-making."

Red flags:
- ❌ "I'd just ignore the NULLs" - no documentation or thought
- ❌ "I'd delete rows with NULL" - doesn't consider business impact
- ❌ No answer / blank stare - encourage them: "What would you want to know before deciding?"

### Follow-Up Probes (Choose Based on Their Answer)

**If they mention COALESCE or similar:**
- "Great! Show me what that SQL would look like."
```sql
SELECT
    COALESCE(customer_state, 'Unknown') AS state,
    SUM(total_amount) AS revenue
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
GROUP BY COALESCE(customer_state, 'Unknown');
```

**If they talk about data quality investigation:**
- "That's excellent data thinking! What specific checks would you run?"
  - Expected: Check created_date (are NULLs recent?), check order counts (do they order more/less?), check customer_city (is it also NULL?)

**If they struggle:**
- Prompt: "Think about the stakeholder looking at your report. They see revenue for 'California', 'Texas', etc. Do they know that 10% is missing?"

### This is a Discussion - Be Flexible!

- Let them think out loud
- Ask follow-ups to dig deeper
- Look for: awareness, reasoning, communication, not perfection

---

## SCORING RUBRIC

Use this to evaluate overall performance. Share this structure with students after the interview.

### Technical Correctness (40 points)

| Question | Points | Criteria |
|----------|--------|----------|
| Q1 | 8 pts | Correct SELECT, WHERE with multiple conditions, ORDER BY |
| Q2 | 16 pts | Correct 3-table JOIN, proper GROUP BY, COUNT(DISTINCT), revenue calculation |
| Q3 | 16 pts | LEFT JOIN anti-pattern OR valid alternative (NOT IN/EXISTS), correct NULL check |

**Deductions:**
- Syntax errors that would prevent query from running: -2 pts per query
- Wrong logic but shows understanding: -1 to -2 pts
- Critical conceptual error (e.g., = NULL): -3 pts

### SQL Best Practices (20 points)

- **Readability (8 pts):** Proper formatting, clear aliases, indentation even on whiteboard
- **Efficiency awareness (6 pts):** Uses WHERE before HAVING, COUNT(DISTINCT) appropriately
- **NULL handling (6 pts):** Uses IS NULL correctly, aware of NULL behavior

### Communication & Process (25 points)

- **Thinking out loud (10 pts):** Explains approach, talks through logic
- **Asks clarifying questions (8 pts):** Confirms understanding, asks about edge cases
- **Handles feedback (7 pts):** Responds well to probes, adjusts when nudged

### Data & Business Thinking (15 points)

- **Q4 responses (10 pts):** Shows awareness of NULL impact, business communication
- **Edge case awareness (5 pts):** Mentions data quality, considers implications throughout

### Total: 100 points

**Scoring bands:**
- **85-100:** Exceptional - ready for FAANG technical screen
- **70-84:** Strong - solid SQL skills, minor improvements
- **55-69:** Competent - understands concepts, needs practice
- **Below 55:** Needs review - revisit fundamentals

---

## POST-INTERVIEW: Providing Feedback (1-2 minutes)

### What to Say

**If they did well (70+):**
> "Nice work! Your SQL fundamentals are solid. Your [JOIN logic / NULL handling / communication] was especially strong. One thing to keep practicing: [pick 1 area]. Overall, you're well-prepared for technical interviews."

**If they struggled (55-69):**
> "You've got the core concepts down, which is great. I'd recommend practicing [JOINs / aggregation / anti-join patterns] a bit more. Specifically, focus on [pick 1-2 areas]. The data thinking in Question 4 was [positive note]. Keep practicing and you'll be ready!"

**If they really struggled (<55):**
> "I can see you understand some basics, which is a good start. Before interview season, I'd recommend reviewing [Day 1/Day 2 materials]. Focus especially on [NULL handling / JOIN types / GROUP BY]. Come to office hours if you want to walk through these concepts together."

### Always End Positively

- "These interviews are hard—you did great coming in and trying!"
- "This is practice. Every time you do this, you get better."
- "The fact that you're doing this now means you'll be way more prepared than most candidates."

---

## QUICK REFERENCE: Key Things to Watch For

### Critical Concepts
- ✅ NULL: IS NULL, not = NULL
- ✅ JOINs: Understanding INNER vs LEFT
- ✅ Aggregation: COUNT(*) vs COUNT(DISTINCT)
- ✅ Anti-join: LEFT JOIN + IS NULL pattern

### Green Flags (Strong Candidate)
- Asks clarifying questions before writing SQL
- Talks through approach first
- Formats SQL clearly even on whiteboard
- Self-corrects when they catch mistakes
- Mentions edge cases (NULL, duplicates)

### Red Flags (Needs More Practice)
- Uses = NULL anywhere
- Doesn't understand why COUNT(DISTINCT) matters
- Can't explain JOIN differences
- Silent—doesn't communicate thinking
- Gives up quickly when stuck

---

## APPENDIX: Quick Verification Queries

Run these on your laptop if you want to double-check their logic:

### Check: How many customers in California?
```python
con.execute("SELECT COUNT(*) FROM customers WHERE customer_state = 'CA'").df()
```

### Check: Orders in March 2024
```python
con.execute("""
    SELECT COUNT(*)
    FROM orders
    WHERE order_date >= '2024-03-01' AND order_date < '2024-04-01'
""").df()
```

### Check: Revenue by category (Q2 answer)
```python
con.execute("""
    SELECT p.category, SUM(oi.price * oi.quantity) AS revenue
    FROM order_items oi
    JOIN products p ON oi.product_id = p.product_id
    JOIN orders o ON oi.order_id = o.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY p.category
    ORDER BY revenue DESC
""").df()
```

---

## End of Interviewer Guide

**Remember:** Be encouraging, be clear, and focus on learning. This is practice for them, and they'll remember how you made them feel more than their exact score.

Good luck with the interviews! 🎯
