# Day 1, Block B: SQL I with DuckDB - SPECIFICATION

**Course:** ECBS5294 - Introduction to Data Science: Working with Data
**Duration:** 90 minutes (15:30–17:10)
**Prerequisites:** Day 1 Block A completed (tidy data concepts, types, primary keys)
**Deliverable:** HW1 assigned (due Day 2 start of class)

---

## 📋 Overview

This block introduces students to SQL using DuckDB, focusing on single-table queries and a scoped primer on window functions. By the end, students should be comfortable with basic SQL and understand when/how to use window functions for common analytics tasks.

**Why DuckDB?**
- Lightweight, no server setup required
- Fast on CSVs and Parquet files
- Full SQL support including window functions
- Perfect for analytics (vs. transactional databases)
- Students can run it locally in Python or CLI

---

## 🎯 Learning Objectives

By the end of Block B, students will be able to:

1. **Explain why SQL is valuable** for data analysis (set-based operations, declarative)
2. **Write basic SQL queries** using SELECT, WHERE, ORDER BY, and calculated columns
3. **Aggregate data** using GROUP BY/HAVING with COUNT, SUM, AVG, MIN, MAX
4. **Handle NULL values** correctly in WHERE clauses and aggregations
5. **Apply window functions** for common analytics:
   - `ROW_NUMBER()` for deduplication and "latest record per group"
   - `LAG()` for period-over-period calculations
   - Moving averages with `ROWS BETWEEN`
6. **Articulate the mental model:** Windows preserve row count; GROUP BY collapses rows
7. **Write queries** that answer business questions (not just technical exercises)

---

## 📚 Key Concepts to Teach

### 1. Why SQL? (5 minutes)

**Hook:**
> "SQL lets you ask questions of data in the language of business logic, not programming loops."

**Key points:**
- **Declarative:** Say *what* you want, not *how* to get it
- **Set-based:** Operate on entire sets of rows at once (vs. row-by-row loops)
- **Standard:** SQL skills transfer across systems (PostgreSQL, MySQL, BigQuery, etc.)
- **Optimized:** Database engines optimize queries automatically
- **Foundation:** Required for joins (Day 2), CTEs, subqueries

**Example:**
```python
# Python (procedural)
total = 0
for row in data:
    if row['category'] == 'Coffee':
        total += row['price']

# SQL (declarative)
SELECT SUM(price)
FROM data
WHERE category = 'Coffee'
```

---

### 2. DuckDB Basics (10 minutes)

**Setup:**
```python
import duckdb

# Connect to in-memory database
con = duckdb.connect(':memory:')

# Query CSV directly (no loading!)
result = con.execute("SELECT * FROM 'data/file.csv' LIMIT 5").df()

# Or load into a table
con.execute("CREATE TABLE sales AS SELECT * FROM 'data/file.csv'")
```

**Key features:**
- Query files directly (CSV, Parquet)
- Results as pandas DataFrame
- Fast analytical queries
- Full SQL support

**Student benefit:** No database setup, just pip install duckdb

---

### 3. Core SQL (25 minutes)

#### SELECT and WHERE
```sql
-- Basic selection
SELECT item, price, quantity
FROM cafe_sales
WHERE price > 5.00;

-- Multiple conditions
SELECT item, price
FROM cafe_sales
WHERE category = 'Coffee'
  AND price BETWEEN 3.00 AND 5.00;

-- Pattern matching
SELECT item
FROM cafe_sales
WHERE item LIKE '%Latte%';
```

**Key concepts:**
- Column selection vs. row filtering
- Comparison operators (=, <, >, <=, >=, !=)
- Logical operators (AND, OR, NOT)
- IN, BETWEEN, LIKE

#### Calculated Columns
```sql
-- Create new columns in results
SELECT
    item,
    price,
    quantity,
    price * quantity AS total,
    price * quantity * 0.1 AS tax
FROM cafe_sales;
```

#### ORDER BY
```sql
-- Sort results
SELECT item, price
FROM cafe_sales
ORDER BY price DESC;

-- Multiple sort keys
SELECT item, category, price
FROM cafe_sales
ORDER BY category ASC, price DESC;
```

**Key concept:** ORDER BY happens last (after filtering, after grouping)

#### NULL Handling
```sql
-- NULLs in WHERE
SELECT *
FROM cafe_sales
WHERE payment_method IS NULL;  -- Not = NULL!

SELECT *
FROM cafe_sales
WHERE payment_method IS NOT NULL;

-- NULL behavior in comparisons
WHERE price > 5.00  -- Excludes NULLs automatically
```

**Critical teaching point:** NULL is not equal to anything, not even NULL!

---

### 4. Aggregations and GROUP BY (20 minutes)

#### Aggregate Functions
```sql
-- Summary statistics
SELECT
    COUNT(*) AS total_transactions,
    COUNT(payment_method) AS known_payment,  -- Excludes NULLs
    SUM(total_spent) AS total_revenue,
    AVG(total_spent) AS avg_transaction,
    MIN(transaction_date) AS first_sale,
    MAX(transaction_date) AS last_sale
FROM cafe_sales;
```

**Key concept:** Aggregates collapse many rows into one row

#### GROUP BY
```sql
-- Aggregate by category
SELECT
    item,
    COUNT(*) AS transaction_count,
    SUM(total_spent) AS total_revenue,
    AVG(total_spent) AS avg_revenue
FROM cafe_sales
GROUP BY item
ORDER BY total_revenue DESC;
```

**Mental model:** "For each [group], calculate [aggregate]"

#### HAVING
```sql
-- Filter groups (not rows!)
SELECT
    item,
    COUNT(*) AS transaction_count,
    SUM(total_spent) AS total_revenue
FROM cafe_sales
GROUP BY item
HAVING COUNT(*) > 100  -- Filter groups
ORDER BY total_revenue DESC;
```

**Key distinction:**
- WHERE filters **rows** before grouping
- HAVING filters **groups** after aggregation

#### NULL in Aggregates
```sql
-- COUNT(*) counts all rows
-- COUNT(column) excludes NULLs
SELECT
    payment_method,
    COUNT(*) AS all_rows,
    COUNT(location) AS with_location
FROM cafe_sales
GROUP BY payment_method;
```

**Critical:** Students need to understand NULL behavior in aggregations!

---

### 5. Window Functions Primer (25 minutes)

**Frame this carefully:**
> "Window functions are like GROUP BY's more flexible cousin. They calculate aggregates but keep all your rows."

#### Mental Model: Preserving Rows

```sql
-- GROUP BY: Collapses rows
SELECT
    item,
    COUNT(*) AS count
FROM cafe_sales
GROUP BY item;
-- Result: One row per item

-- Window function: Keeps all rows
SELECT
    transaction_id,
    item,
    COUNT(*) OVER (PARTITION BY item) AS item_count
FROM cafe_sales;
-- Result: Original row count, with count added to each row
```

**Key insight:** Windows preserve row count; GROUP BY collapses.

#### Use Case 1: ROW_NUMBER() for Deduplication

**Business problem:** "I want the most recent transaction per customer"

```sql
-- Rank transactions per customer by date
SELECT
    customer_id,
    transaction_date,
    total_spent,
    ROW_NUMBER() OVER (
        PARTITION BY customer_id
        ORDER BY transaction_date DESC
    ) AS row_num
FROM customer_transactions;

-- Get only the latest
SELECT *
FROM (
    SELECT
        customer_id,
        transaction_date,
        total_spent,
        ROW_NUMBER() OVER (
            PARTITION BY customer_id
            ORDER BY transaction_date DESC
        ) AS row_num
    FROM customer_transactions
)
WHERE row_num = 1;
```

**Key concepts:**
- `PARTITION BY` = "for each customer"
- `ORDER BY` within OVER = how to rank
- Filter row_num = 1 to get latest

**Alternative framing:** "Latest order status per customer", "Most recent login per user"

#### Use Case 2: LAG() for Period-over-Period Change

**Business problem:** "What's the month-over-month change in sales?"

```sql
-- Calculate previous month's sales
SELECT
    month,
    total_sales,
    LAG(total_sales, 1) OVER (ORDER BY month) AS prev_month_sales,
    total_sales - LAG(total_sales, 1) OVER (ORDER BY month) AS change
FROM monthly_sales
ORDER BY month;
```

**Key concepts:**
- `LAG(column, n)` = value from n rows before
- `LEAD(column, n)` = value from n rows after
- Order matters! Must ORDER BY time dimension

**Business framing:** "Growth rates", "Before and after comparisons"

#### Use Case 3: Moving Average

**Business problem:** "Smooth out daily volatility with a 7-day moving average"

```sql
-- 7-day moving average of sales
SELECT
    date,
    daily_sales,
    AVG(daily_sales) OVER (
        ORDER BY date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS moving_avg_7day
FROM daily_sales
ORDER BY date;
```

**Key concepts:**
- `ROWS BETWEEN` defines the window frame
- `6 PRECEDING AND CURRENT ROW` = 7 rows total (6 before + current)
- Order determines which rows are "preceding"

**Business framing:** "Smoothing trends", "Seasonal patterns"

#### Window Function Syntax Breakdown

```sql
<function>() OVER (
    [PARTITION BY column]    -- Optional: Define groups
    [ORDER BY column]        -- Optional: Define order within groups
    [ROWS BETWEEN ... ]      -- Optional: Define frame
)
```

**Common gotchas to teach:**
- Forgetting ORDER BY when order matters (ROW_NUMBER, LAG, moving average)
- Mixing window functions with GROUP BY (advanced, skip for now)
- Not understanding frame defaults (important but can skip in primer)

---

## 🎓 Session Flow (90 minutes)

### Segment 1: Introduction (5 min)
- Why SQL matters for data analysts
- Why DuckDB (lightweight, fast, analytical)
- Connection to Block A: We cleaned the data, now let's query it!

### Segment 2: DuckDB Setup & First Query (10 min)
- Install duckdb in notebook
- Connect to database
- Query the cafe sales CSV directly
- Get results as DataFrame

### Segment 3: Core SQL - SELECT, WHERE, ORDER BY (15 min)
- Basic SELECT syntax
- Filtering with WHERE
- Calculated columns
- Sorting with ORDER BY
- NULL handling in WHERE clauses
- **Quick exercise:** Write 3 queries from prompts

### Segment 4: Aggregations & GROUP BY (15 min)
- Aggregate functions (COUNT, SUM, AVG, MIN, MAX)
- GROUP BY concept and syntax
- HAVING for filtering groups
- WHERE vs. HAVING
- NULL behavior in aggregates
- **Quick exercise:** Answer business questions with aggregations

### Segment 5: Window Functions Primer (25 min)
- Mental model: Windows vs. GROUP BY
- ROW_NUMBER() for "latest per group"
- LAG() for period-over-period
- Moving average with ROWS BETWEEN
- Common patterns and gotchas
- **Quick exercise:** Apply window functions

### Segment 6: HW1 Assignment & Wrap (10 min)
- Describe HW1 structure
- Dataset overview
- Questions preview
- Submission instructions
- Due date: Day 2 start of class

### Segment 7: Optional Lab Time (10 min if time)
- Students start on HW1 if time permits
- Instructor available for questions

---

## 📦 Materials to Create

### 1. Teaching Notebook
**File:** `notebooks/day1_block_b_sql_intro.ipynb`

**Structure:**
1. **Section 1:** Why SQL & DuckDB Setup
   - Installation instructions
   - Connection examples
   - First query
2. **Section 2:** SELECT, WHERE, ORDER BY
   - Basic syntax with examples
   - NULL handling
   - 3-5 example queries with business context
3. **Section 3:** Calculated Columns
   - Creating new columns
   - Common calculations
   - Aliases
4. **Section 4:** Aggregations
   - COUNT, SUM, AVG, MIN, MAX
   - NULL behavior demonstrations
5. **Section 5:** GROUP BY and HAVING
   - Grouping concept
   - Multiple aggregates
   - WHERE vs HAVING
   - Examples with business questions
6. **Section 6:** Window Functions Primer
   - Mental model explanation
   - ROW_NUMBER() with examples
   - LAG() with examples
   - Moving average with examples
   - Common patterns
7. **Section 7:** Putting It Together
   - Multi-step query examples
   - Business question → SQL translation
   - Preview of HW1

**Key requirements:**
- All code must be executable
- Use cafe sales dataset from Block A
- Business context for every query (not just "SELECT * FROM...")
- Clear explanations of output
- Visual comparisons (DataFrame display)
- Emphasize "Why?" and "When?" not just "How?"

---

### 2. Practice Dataset
**File:** `data/day1/cafe_sales_for_sql.csv` or use existing dirty_cafe_sales.csv

**Option A:** Use cleaned version of Block A dataset
- Pros: Continuity, students already familiar
- Cons: May need to clean it first in notebook

**Option B:** Create separate clean SQL practice dataset
- Pros: Ready to query immediately
- Cons: Another dataset to manage

**Recommendation:** Use Block A dataset, add 2-3 cells at top of teaching notebook to do quick cleaning (convert types, handle nulls). Shows "SQL works on clean data."

**Additional dataset needed:**
**File:** `data/day1/customer_transactions.csv` (for window function examples)
- ~200-500 rows
- Columns: customer_id, transaction_date, transaction_id, total_spent
- Multiple transactions per customer
- Time series data (dates spanning 3-6 months)
- Some customers with 1 transaction, some with many (for ROW_NUMBER example)

---

### 3. HW1 Assignment

**Directory:** `assignments/hw1/`

**Files needed:**

#### `assignments/hw1/README.md`
- Assignment description
- Learning objectives
- Dataset description
- Questions/tasks
- Submission instructions
- Rubric
- Due date

#### `assignments/hw1/hw1_starter.ipynb`
- Pre-structured notebook
- TODO sections for each question
- Markdown explanations of what's expected
- Code cell templates
- Runs successfully when complete

#### `assignments/hw1/data/hw1_dataset.csv`
- Clean dataset for homework (different from teaching examples)
- Suggestion: Use a retail or e-commerce dataset
- Should support:
  - Single-table queries
  - Aggregations
  - Window functions (latest order per customer, month-over-month growth)
- Size: 500-2000 rows (not too large)

#### `assignments/hw1/hw1_solution.ipynb` (don't distribute to students!)
- Complete solution
- For instructor/TA grading reference
- Annotations explaining common mistakes

**Assignment Structure (suggested):**

**Part 1: Basic Queries (30 points)**
- 3-4 SELECT/WHERE/ORDER BY questions
- Examples:
  - "Find all transactions over $50"
  - "List products in a category, sorted by price"
  - "Count transactions with NULL payment method"

**Part 2: Aggregations (40 points)**
- 3-4 GROUP BY questions
- Examples:
  - "Total revenue by product category"
  - "Average order value by month"
  - "Top 10 customers by total spent"
  - "Products with more than 50 transactions"

**Part 3: Window Functions (30 points)**
- 2-3 window function questions
- Examples:
  - "Latest order date per customer using ROW_NUMBER()"
  - "Month-over-month sales change using LAG()"
  - "7-day moving average of daily revenue"

**Bonus (10 points, optional):**
- Complex query combining concepts
- Example: "For each product category, show the product with highest revenue and its rank"

**Rubric (per question):**
- Correctness (40%): Query produces correct results
- Data thinking (25%): Shows understanding of SQL concepts
- Code quality (20%): Clean, readable, commented
- Communication (15%): Markdown cells explain reasoning

---

### 4. Quick Reference Card (Optional but Recommended)
**File:** `references/sql_quick_reference.md`

**Contents:**
- SQL query structure (SELECT, FROM, WHERE, GROUP BY, HAVING, ORDER BY)
- Common aggregate functions
- Window function syntax
- NULL handling rules
- WHERE vs HAVING
- Common patterns (latest per group, period change, moving avg)
- DuckDB-specific tips

---

### 5. Teacher Guide (Similar to Block A)
**File:** `references/teaching/day1_block_b_teacher_primer.md`

**Contents:**
- Learning objectives
- Session flow with timing
- Common student questions and answers
- Window functions teaching tips (this is the hard part!)
- Assessment guidance
- Connection to Block A concepts
- Preview of Day 2 (joins)

**Key teaching notes to include:**
- **Window functions are the challenge:** Most students won't have seen these before
- **Mental model is crucial:** "Preserves rows vs. collapses rows"
- **Use business examples:** Not just technical syntax
- **Build incrementally:** First show GROUP BY, then show window equivalent
- **ROW_NUMBER is easiest:** Start here, then LAG, then moving average
- **ORDER BY matters:** Emphasize when ORDER BY in OVER clause is required

---

## 🎯 Pedagogical Guidance for TA

### Teaching Window Functions to Beginners

**The Challenge:**
Window functions are conceptually harder than GROUP BY. Students who just learned GROUP BY may be confused about when to use windows vs. grouping.

**The Approach:**
1. **Start with the problem:** "I want to see each transaction AND the total for that item"
2. **Show GROUP BY limitation:** It collapses rows, lose transaction detail
3. **Introduce window functions:** "Windows let you add aggregates WITHOUT collapsing"
4. **Visual comparison:** Show same data with GROUP BY vs. window side-by-side
5. **Three use cases:** Latest-per-group, period-change, moving average
6. **Emphasize "when":** When do you use windows vs. GROUP BY?

**Common Student Questions:**

**Q: "When do I use GROUP BY vs. window functions?"**
A: If you want one row per group (summary), use GROUP BY. If you want all rows with a calculation added, use windows.

**Q: "What does PARTITION BY do?"**
A: It's like GROUP BY for window functions. "For each X, calculate Y."

**Q: "Why do I need ORDER BY in OVER?"**
A: Some functions (ROW_NUMBER, LAG, moving average) need to know the order. Others don't (like COUNT, SUM).

**Q: "What's the difference between ROW_NUMBER(), RANK(), and DENSE_RANK()?"**
A: For primer, stick to ROW_NUMBER(). Mention others exist but skip details.

**Q: "Can I use window functions and GROUP BY together?"**
A: Yes, but it's advanced. Skip for now. (Show in Day 2 or later if needed.)

### Teaching Progression

**Don't teach this way (too abstract):**
> "A window function performs a calculation across a set of rows that are somehow related to the current row..."

**Do teach this way (concrete problem first):**
> "Let's say you want to find the latest transaction for each customer. With GROUP BY, you'd get one row per customer. But what if you want to see ALL transactions and mark which one is the latest? That's what ROW_NUMBER() does."

### Code Examples Should Be Business-Focused

❌ **Bad (too abstract):**
```sql
SELECT id, value,
       ROW_NUMBER() OVER (PARTITION BY category ORDER BY value DESC) as rn
FROM table1;
```

✅ **Good (business context):**
```sql
-- Find the most expensive item in each category
-- ROW_NUMBER ranks items within each category by price
SELECT
    item_name,
    category,
    price,
    ROW_NUMBER() OVER (
        PARTITION BY category
        ORDER BY price DESC
    ) AS price_rank
FROM products;

-- Then filter to rank = 1 to get the top item per category
```

---

## 📊 Dataset Requirements Summary

### Primary Dataset (Teaching)
- **Source:** Cleaned version of Block A cafe_sales
- **Size:** 1000-10000 rows
- **Must have:**
  - Categorical columns (for GROUP BY)
  - Numeric columns (for aggregations)
  - Date column (for ORDER BY, time-based analysis)
  - Some NULLs (to teach NULL handling)

### Secondary Dataset (Window Functions)
- **Purpose:** Customer transactions over time
- **Size:** 200-500 rows
- **Must have:**
  - customer_id (for PARTITION BY)
  - transaction_date (for ORDER BY)
  - Multiple transactions per customer (for ROW_NUMBER)
  - Time series spanning months (for LAG, moving average)

### HW1 Dataset
- **Purpose:** Different domain from teaching examples
- **Suggestion:** E-commerce orders, gym membership check-ins, library book checkouts
- **Size:** 500-2000 rows
- **Must support:** All query types in assignment

**Where to find datasets:**
- Kaggle (cleaned versions)
- Generate synthetic data (Python script)
- Use DuckDB's sample datasets if available

---

## ✅ Deliverables Checklist for TA

### Must Have (MVP)
- [ ] `notebooks/day1_block_b_sql_intro.ipynb` - Teaching notebook
- [ ] `data/day1/customer_transactions.csv` - Window functions dataset
- [ ] `assignments/hw1/README.md` - Assignment description
- [ ] `assignments/hw1/hw1_starter.ipynb` - Student starter notebook
- [ ] `assignments/hw1/data/hw1_dataset.csv` - Homework dataset
- [ ] `assignments/hw1/hw1_solution.ipynb` - Solution (for grading)

### Should Have
- [ ] `references/teaching/day1_block_b_teacher_primer.md` - Teaching guide
- [ ] `references/sql_quick_reference.md` - Student reference card

### Nice to Have
- [ ] Slide deck for teaching (if preferred)
- [ ] Video walkthrough of teaching notebook
- [ ] Extra practice problems

---

## 🎨 Style Guidelines

**Follow Block A patterns:**
- Use same markdown structure in notebooks
- Same header format: "# Day 1, Block B: SQL I with DuckDB"
- Same TODO style in starter notebooks
- Same assertion patterns for validation
- Same business-focused framing

**DuckDB-specific:**
- Show both Python API and SQL syntax
- Display results as DataFrames (not just raw SQL output)
- Emphasize DuckDB advantages (query files directly, fast)
- Note any DuckDB-specific syntax if different from PostgreSQL

**Code style:**
- Use uppercase for SQL keywords (SELECT, WHERE, FROM)
- Indent for readability
- Comment complex queries
- Use aliases (AS) for clarity

---

## 🔗 Connection to Other Materials

### From Block A
- Students now understand tidy data, types, primary keys
- Use Block A cafe sales dataset (cleaned) for SQL practice
- Reference primary key concept when explaining unique constraints

### To Day 2
- Block B teaches single-table queries
- Day 2 will add JOINs (multi-table)
- Window functions primer in Block B enables more complex joins later
- HW1 due at start of Day 2 (collect before teaching)

---

## ⚠️ Common Pitfalls to Avoid

### For TA Creating Materials

1. **Don't make window functions too complex**
   - Stick to three use cases: ROW_NUMBER, LAG, moving average
   - Skip RANK, DENSE_RANK, complex frames
   - No CTEs with window functions (yet)
   - No mixing window functions with GROUP BY (yet)

2. **Don't use abstract examples**
   - Every query should answer a business question
   - "Find top 10 products" not "SELECT * FROM table1"

3. **Don't forget NULL handling**
   - Students will have NULLs in their data
   - Must teach IS NULL, IS NOT NULL
   - Must teach how aggregates handle NULLs

4. **Don't skip the "why"**
   - Why SQL vs Python for this task?
   - Why window functions vs GROUP BY?
   - Why does order matter in OVER clause?

5. **Don't assume prior SQL knowledge**
   - This is their first exposure to SQL
   - Explain everything, even "obvious" things
   - Show mistakes and how to fix them

### For Students (Put in Materials)

1. **Using = NULL instead of IS NULL**
   - `WHERE column = NULL` doesn't work!
   - Use `WHERE column IS NULL`

2. **Confusing WHERE and HAVING**
   - WHERE filters rows before grouping
   - HAVING filters groups after aggregation

3. **Forgetting ORDER BY in window functions**
   - ROW_NUMBER() needs ORDER BY
   - LAG() needs ORDER BY
   - Otherwise results are unpredictable

4. **Not understanding PARTITION BY**
   - It's optional but powerful
   - Defines the "groups" for window calculation

5. **Expecting window functions to filter rows**
   - Windows preserve all rows
   - Use subquery or CTE to filter after (can show example, mark as advanced)

---

## 📝 Success Criteria

Materials are complete when:

1. ✅ **Teaching notebook runs end-to-end** without errors
2. ✅ **All SQL concepts have business-context examples**
3. ✅ **Window functions explained with mental model first**
4. ✅ **HW1 is clearly specified** with rubric
5. ✅ **Datasets support all teaching examples**
6. ✅ **Solution notebook works** for grading reference
7. ✅ **Materials match Block A quality and style**

Student success when:
- Can write basic SELECT/WHERE/GROUP BY queries
- Can explain when to use WHERE vs HAVING
- Can apply ROW_NUMBER() for "latest per group"
- Can apply LAG() for period-over-period change
- Can explain difference between GROUP BY and windows
- Complete HW1 successfully

---

## 🕐 Estimated Development Time

- Teaching notebook: 3-4 hours
- Datasets (finding/creating): 1-2 hours
- HW1 assignment: 2-3 hours
- Solution notebook: 1-2 hours
- Teacher guide: 1-2 hours
- Reference materials: 1 hour

**Total: 9-14 hours** (depending on experience with DuckDB and window functions)

**Parallelize:**
- Teaching notebook and HW1 can be developed simultaneously
- Datasets can be created early
- Reference materials can be created last

---

## 📚 Resources for TA

### DuckDB Documentation
- https://duckdb.org/docs/
- SQL Introduction: https://duckdb.org/docs/sql/introduction
- Window Functions: https://duckdb.org/docs/sql/window_functions

### SQL Learning Resources
- PostgreSQL Tutorial (window functions): https://www.postgresqltutorial.com/postgresql-window-function/
- Mode Analytics SQL Tutorial: https://mode.com/sql-tutorial/
- Window Functions Explained: https://mjk.space/advances-sql-window-frames/

### Example Datasets
- Kaggle: Search "cleaned" or "SQL practice"
- DuckDB examples: https://github.com/duckdb/duckdb/tree/master/data
- Generate synthetic: Use Faker or similar Python library

---

## 💬 Questions for Instructor (Resolve Before Starting)

1. **Dataset preference:** Use Block A cafe_sales (cleaned) or create new dataset?
2. **HW1 domain:** What domain for homework dataset? (retail, e-commerce, other?)
3. **Window functions depth:** Stick to 3 use cases or add RANK/DENSE_RANK?
4. **Submission format:** How will students submit HW1? (Moodle, GitHub, email?)
5. **Grading:** Will instructor or TA grade HW1?
6. **DuckDB version:** Any specific version requirements?
7. **Python version:** Verify same as Block A (3.8+)?

---

## ✉️ Contact

**Questions during development?**
- Refer to Block A materials as template
- Check DuckDB documentation for syntax
- Test all code in a clean environment
- Ask instructor if conceptual questions arise

---

## 🎯 Final Notes

**Philosophy:**
- SQL is a *thinking tool*, not just a query language
- Window functions are powerful but keep the primer scoped
- Every query should feel like answering a business question
- Build confidence through incremental examples

**Quality Bar:**
- Same level as Block A materials
- Executable, tested, documented
- Beginner-friendly with clear explanations
- Business-focused throughout

**You've got this!** The Block A materials set a great template. Follow that structure, focus on business context, and remember: students are seeing SQL for the first time. Make it approachable and practical.

---

**Status:** SPECIFICATION READY FOR DEVELOPMENT

**Next Step:** TA reviews spec, asks clarifying questions, then begins creating materials.

**Target Completion:** Before Day 1 (Oct 8, 2025)

Good luck! 🚀
