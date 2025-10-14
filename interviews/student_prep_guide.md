# Student Prep Guide: SQL Whiteboard Interview Simulations

**How to Prepare for Your 25-Minute SQL Interview Practice**

---

## Overview

This guide will help you prepare for the whiteboard interview simulation. You'll get the most value if you review these concepts and practice the recommended exercises before your interview.

**Remember:** The goal is learning and preparation, not perfection!

---

## What You'll Be Evaluated On

Your interviewer will assess you across four dimensions:

### 1. **Technical Correctness (40%)**
- Can you write syntactically correct SQL?
- Do your queries return the right results?
- Do you understand what each clause does?

### 2. **SQL Best Practices (20%)**
- Is your SQL readable and well-formatted?
- Do you use WHERE before HAVING?
- Do you handle NULL values correctly?
- Do you use COUNT(DISTINCT) when appropriate?

### 3. **Communication & Process (25%)**
- Do you think out loud?
- Do you ask clarifying questions?
- Can you explain your approach?
- How do you handle feedback?

### 4. **Data & Business Thinking (15%)**
- Do you understand the business context?
- Do you consider edge cases (NULL, zero values)?
- Can you spot data quality issues?
- Do you think beyond the syntax?

---

## Key SQL Concepts to Review

### Core Concepts (Must Know)

#### 1. **SELECT Basics**
```sql
SELECT column1, column2
FROM table_name
WHERE condition
ORDER BY column1 DESC
LIMIT 10;
```

**Practice:** Write a query without looking at your notes.

#### 2. **WHERE vs HAVING**
- **WHERE:** Filters BEFORE aggregation (row-level)
- **HAVING:** Filters AFTER aggregation (group-level)

```sql
-- WHERE: filter rows before grouping
SELECT category, SUM(sales)
FROM orders
WHERE order_date >= '2024-01-01'
GROUP BY category;

-- HAVING: filter groups after aggregation
SELECT category, SUM(sales) AS total_sales
FROM orders
GROUP BY category
HAVING SUM(sales) > 10000;
```

**Common mistake:** Using aggregate functions in WHERE (❌ WHERE SUM(sales) > 1000)

#### 3. **NULL Handling** ⚠️ CRITICAL

**THE #1 MISTAKE BEGINNERS MAKE:**

❌ **NEVER DO THIS:**
```sql
WHERE column = NULL  -- WRONG! This doesn't work!
```

✅ **ALWAYS DO THIS:**
```sql
WHERE column IS NULL
WHERE column IS NOT NULL
```

**Why it matters:**
- NULL means "unknown"
- NULL != NULL (even NULL doesn't equal itself!)
- Comparisons with NULL return NULL (which is falsy in WHERE)

**Practice:**
- What does `SELECT * FROM users WHERE last_login = NULL` return? (Answer: Nothing!)
- How do you find users who HAVE logged in? (Answer: `WHERE last_login IS NOT NULL`)

#### 4. **INNER JOIN vs LEFT JOIN**

**INNER JOIN:** Only rows that match in BOTH tables
```sql
SELECT o.order_id, c.customer_name
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id;
```
- Result: Only orders that have a matching customer
- **Drops** unmatched rows

**LEFT JOIN:** ALL rows from left table + matches from right
```sql
SELECT o.order_id, r.review_score
FROM orders o
LEFT JOIN reviews r ON o.order_id = r.order_id;
```
- Result: All orders, with review_score = NULL for orders without reviews
- **Keeps** all left-side rows

**When to use each:**
- INNER: "Show me only complete pairs"
- LEFT: "Show me everything from the left, with extras from the right if available"

#### 5. **GROUP BY Fundamentals**

**Rule:** Every column in SELECT must be either:
1. In GROUP BY clause, OR
2. Inside an aggregate function (SUM, COUNT, AVG, MIN, MAX)

✅ **Correct:**
```sql
SELECT
    category,                    -- In GROUP BY
    COUNT(*) AS num_orders,      -- Aggregate function
    SUM(amount) AS total_sales   -- Aggregate function
FROM orders
GROUP BY category;               -- Matches SELECT
```

❌ **Wrong:**
```sql
SELECT category, customer_id, COUNT(*)
FROM orders
GROUP BY category;  -- Missing customer_id in GROUP BY!
```

#### 6. **COUNT vs COUNT(DISTINCT)**

After JOINs, be careful!

```sql
-- Without DISTINCT: Counts all rows (inflated by JOIN)
SELECT COUNT(*) FROM orders JOIN order_items ...  -- Might count orders multiple times!

-- With DISTINCT: Counts unique orders
SELECT COUNT(DISTINCT order_id) FROM orders JOIN order_items ...  -- Correct!
```

**When to use:**
- No JOINs? `COUNT(*)` is fine
- After JOINs? Use `COUNT(DISTINCT primary_key)` to avoid inflation

#### 7. **Window Functions** (Advanced)

```sql
SELECT
    user_id,
    total_usage,
    ROW_NUMBER() OVER (PARTITION BY plan_type ORDER BY total_usage DESC) AS rank
FROM user_stats;
```

**Key parts:**
- `ROW_NUMBER()`: Assigns ranks (1, 2, 3...)
- `PARTITION BY`: "Restart ranking for each group"
- `ORDER BY`: "Rank by this column"

**Cannot filter window functions in WHERE!**
```sql
-- ❌ WRONG
WHERE ROW_NUMBER() OVER (...) <= 3

-- ✅ CORRECT
-- Use subquery or CTE, THEN filter
WITH ranked AS (
    SELECT *, ROW_NUMBER() OVER (...) AS rank
    FROM table
)
SELECT * FROM ranked WHERE rank <= 3;
```

---

## Whiteboard-Specific Tips

### Before You Write

1. **Repeat the question back:** "So you want me to find all orders from California with sales over $50K?"
2. **Clarify ambiguities:** "When you say 'active', do you mean end_date is NULL or in the future?"
3. **Sketch your approach:** "I'll need to join orders and customers, then filter for CA and group by store..."

### While You Write

1. **Format clearly, even on a whiteboard:**
```sql
SELECT
    column1,
    column2,
    SUM(column3) AS total
FROM table1 t1
INNER JOIN table2 t2 ON t1.id = t2.id
WHERE condition
GROUP BY column1, column2
ORDER BY total DESC;
```
- Indent for readability
- One clause per line when possible
- Use aliases (t1, t2) consistently

2. **Talk through your logic:**
- "First, I'm joining these two tables on customer_id..."
- "I'm using WHERE here because I need to filter before aggregation..."
- "I'm checking for NULL last_login because some users might not have logged in yet..."

3. **Check for common mistakes:**
- ✅ Did I use IS NULL (not = NULL)?
- ✅ Did I use HAVING for aggregate filters?
- ✅ Do I need COUNT(DISTINCT) after a JOIN?
- ✅ Is every SELECT column in GROUP BY or an aggregate?

### After You Write

1. **Trace through your query:** "This will first join... then filter... then group... then order..."
2. **Consider edge cases:** "If there are no orders in April, this would return zero rows."
3. **Ask yourself:** "Does this answer the business question?"

---

## Practice Exercises

### Exercise 1: Write SQL on Paper (30 minutes)

Take a piece of paper (no computer!) and write SQL queries for these questions:

Given tables: `employees (employee_id, name, department, salary, hire_date)` and `departments (department_id, department_name, location)`

1. Find all employees hired in 2023 with salary > $70K
2. Count employees by department
3. Find departments with average salary > $80K
4. Find the top 3 highest-paid employees per department (use window functions)
5. Find employees whose department has NULL location

Check your answers later by running them in DuckDB or SQLite.

### Exercise 2: Practice Talking Out Loud (15 minutes)

Pick a SQL query from Day 1 or Day 2 notebooks. Cover it up, then:
1. Read only the business question
2. Say OUT LOUD (seriously, speak!) how you'd solve it
3. Write the query while narrating each step
4. Compare your answer to the notebook

This will feel awkward. That's the point. Interviews are awkward!

### Exercise 3: Debug These Broken Queries (20 minutes)

Find the mistakes:

**Query 1:**
```sql
SELECT category, product_name, SUM(sales)
FROM products
GROUP BY category;
```
(Hint: product_name isn't aggregated or in GROUP BY!)

**Query 2:**
```sql
SELECT *
FROM orders
WHERE customer_id = NULL;
```
(Hint: = NULL doesn't work!)

**Query 3:**
```sql
SELECT customer_id, COUNT(order_id)
FROM orders
GROUP BY customer_id
WHERE COUNT(order_id) > 5;
```
(Hint: WHERE should be HAVING!)

**Query 4:**
```sql
SELECT o.order_id, COUNT(*) AS num_items
FROM orders o
INNER JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY o.order_id
ORDER BY num_items DESC;
```
(Trick question: This one is actually correct! Did you check for false positives?)

---

## Review Checklist

Before your interview, make sure you can:

### SQL Fundamentals
- [ ] Write SELECT, WHERE, ORDER BY without notes
- [ ] Explain the difference between WHERE and HAVING
- [ ] Use IS NULL and IS NOT NULL correctly
- [ ] Use BETWEEN, IN, LIKE for filtering

### JOINs
- [ ] Write an INNER JOIN
- [ ] Write a LEFT JOIN
- [ ] Explain when to use each
- [ ] Join on multiple columns (e.g., store_id AND product_id)

### Aggregation
- [ ] Use COUNT, SUM, AVG, MIN, MAX
- [ ] Write correct GROUP BY clauses
- [ ] Use HAVING to filter aggregated results
- [ ] Use COUNT(DISTINCT) to avoid duplication

### Advanced (If Covered in Class)
- [ ] Write a CTE (WITH clause)
- [ ] Use ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ...)
- [ ] Filter window function results with subquery

### Business Thinking
- [ ] Ask clarifying questions when requirements are ambiguous
- [ ] Consider NULL values in your queries
- [ ] Think about what happens with zero-match JOINs
- [ ] Explain your query in business terms ("This shows revenue by region...")

---

## Common Mistakes to Avoid

### Technical Mistakes

1. **= NULL instead of IS NULL** ← #1 killer!
2. **Aggregate in WHERE instead of HAVING**
3. **Missing columns from GROUP BY**
4. **Forgetting COUNT(DISTINCT) after JOINs**
5. **Using wrong JOIN type** (INNER when you need LEFT)

### Communication Mistakes

1. **Silence** - Not explaining your thinking
2. **Rushing** - Writing before understanding the question
3. **Defensiveness** - Getting upset when stuck
4. **Assuming** - Not asking clarifying questions

---

## Day Before Checklist

- [ ] Review Day 1, Block B notebooks (SQL Foundations, Aggregations, Window Functions)
- [ ] Review Day 2, Block A notebook (JOINs)
- [ ] Practice writing 2-3 queries on paper
- [ ] Practice explaining a query out loud
- [ ] Get a good night's sleep (seriously!)
- [ ] Eat beforehand (don't interview hungry!)

---

## Day of Interview

### What to Bring
- ✅ Yourself (on time!)
- ✅ Positive attitude
- ✅ Willingness to think out loud

### What NOT to Bring
- ❌ Laptop
- ❌ Notes or cheat sheets
- ❌ Phone (or keep it silenced/away)

### Mental Prep
- This is PRACTICE, not a real interview
- Making mistakes is the point—you're here to learn
- Your instructor wants you to succeed
- Struggling is normal and expected
- You know more than you think!

---

## During the Interview

### If You Get Stuck

1. **Don't panic silently!** Say: "I'm not sure about this part. Let me think through it..."
2. **Ask for a hint:** "Can you remind me the syntax for LEFT JOIN?"
3. **Talk through what you DO know:** "I know I need to join these tables, I'm just not sure which type of join..."
4. **Break it down:** "Let me start with the simpler part first..."

### If You Make a Mistake

1. **It's okay!** Everyone makes mistakes in interviews.
2. **If you catch it, fix it:** "Oh wait, I should use IS NULL here, not = NULL."
3. **If the interviewer points it out, learn from it:** "Ah, right! Thanks for catching that."
4. **Don't dwell on it—move forward.**

---

## After the Interview

### Immediate Actions

1. **Write down** the questions you struggled with
2. **Review** the concepts you missed
3. **Practice** those specific areas

### If You Want More Feedback

- Come to office hours
- Ask specific questions: "I struggled with JOINs—can we review that?"
- Practice more and consider doing another simulation (if slots are available)

---

## Final Pep Talk

**You've got this!**

You've learned a TON of SQL in this class. The whiteboard format is new and challenging, but the concepts are the same ones you've been practicing.

The students who succeed in these simulations are NOT the ones who know the most SQL—they're the ones who:
- Think out loud
- Ask clarifying questions
- Stay calm when stuck
- Learn from mistakes

Be one of those students.

See you at the whiteboard! 🎯📝

---

**Questions?**
- Email: RubiaE@ceu.edu
- Office Hours: [Check syllabus]
- Moodle Forum: Post your prep questions!
