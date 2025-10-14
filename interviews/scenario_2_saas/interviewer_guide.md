# Scenario 2: SaaS Product Analytics
## Whiteboard Interview Simulation - Interviewer Guide

**Duration:** 25 minutes
**Difficulty:** Intermediate
**Focus:** Date calculations, window functions, subscription analytics, business metrics

---

## Overview

This scenario simulates a data analyst interview at a B2B SaaS company (think Slack, Asana, or Tableau). Students will analyze user behavior, subscriptions, and feature usage. This scenario introduces concepts common in subscription business models.

**Key Learning Objectives:**
- Date arithmetic and comparisons
- Subscription business logic (active vs churned)
- Window functions (ROW_NUMBER, PARTITION BY)
- Feature usage analytics
- MRR (Monthly Recurring Revenue) calculations

---

## Pre-Interview Setup (5 minutes before student arrives)

### 1. Load Sample Data on Your Laptop

```bash
cd /Users/earino/CEU/ECBS5294/interviews/scenario_2_saas
```

In Python/Jupyter:
```python
import duckdb
import datetime
con = duckdb.connect(':memory:')

# Load all tables
con.execute("CREATE TABLE users AS SELECT * FROM 'data/users.csv'")
con.execute("CREATE TABLE subscriptions AS SELECT * FROM 'data/subscriptions.csv'")
con.execute("CREATE TABLE feature_usage AS SELECT * FROM 'data/feature_usage.csv'")
con.execute("CREATE TABLE support_tickets AS SELECT * FROM 'data/support_tickets.csv'")

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
| 2-6 min | Question 1 (warm-up: active subscriptions) |
| 6-12 min | Question 2 (MRR calculation) |
| 12-19 min | Question 3 (inactive users with date math) |
| 19-24 min | Question 4 (window functions: top users per tier) |
| 24-25 min | Wrap-up, feedback |

---

## PART 1: Scenario Introduction (0-2 minutes)

### Script (Read to Student)

> "Welcome! This is a SQL whiteboard interview simulation for a Data Analyst role at **DataFlow**, a B2B SaaS company that provides project management software. Companies subscribe to DataFlow, and their users log in to use various features like task management, reporting, and collaboration tools.
>
> Your stakeholder is the VP of Product, and they're preparing for a board meeting. They need insights about user engagement and subscription health.
>
> You'll work with four tables: `users`, `subscriptions`, `feature_usage`, and `support_tickets`. Let me draw the schema..."

### Draw This Schema on Whiteboard

```
┌─────────────────────────┐
│        users            │
│─────────────────────────│
│ user_id (VARCHAR)       │ PK
│ company_id (VARCHAR)    │
│ email (VARCHAR)         │
│ signup_date (DATE)      │
│ last_login (DATE)       │  ⚠️ Some users haven't logged in recently
└─────────────────────────┘
           │
           │ 1:many
           │
┌──────────▼──────────────┐
│   subscriptions         │
│─────────────────────────│
│ subscription_id (VARCHAR)│ PK
│ company_id (VARCHAR)    │ FK
│ plan_type (VARCHAR)     │  'starter', 'professional', 'enterprise'
│ monthly_price (DECIMAL) │
│ start_date (DATE)       │
│ end_date (DATE)         │  ⚠️ NULL = active subscription
└─────────────────────────┘
           │
           │
           │
┌──────────▼──────────────┐
│   feature_usage         │
│─────────────────────────│
│ usage_id (VARCHAR)      │ PK
│ user_id (VARCHAR)       │ FK
│ feature_name (VARCHAR)  │  'tasks', 'reports', 'collaboration'
│ usage_date (DATE)       │
│ usage_count (INTEGER)   │  # of times feature used that day
└─────────────────────────┘


┌─────────────────────────┐
│   support_tickets       │
│─────────────────────────│
│ ticket_id (VARCHAR)     │ PK
│ user_id (VARCHAR)       │ FK
│ created_date (DATE)     │
│ status (VARCHAR)        │  'open', 'in_progress', 'resolved'
│ priority (VARCHAR)      │  'low', 'medium', 'high'
└─────────────────────────┘
```

### Explain Key Points

- **company_id** links users to subscriptions (one company, many users)
- **plan_type** has three tiers: 'starter', 'professional', 'enterprise'
- **end_date** in subscriptions: **NULL means active**, a date means churned
- **last_login** in users: when the user last accessed the platform
- **Today's date** for this scenario: **2024-04-15**

**Say to student:** "Any questions about the data model?"

---

## QUESTION 1: Warm-Up (2-6 minutes)

### The Question

> "Let's start simple. How many **active subscriptions** do we have as of today (April 15, 2024)? Remember, an active subscription has a NULL end_date or an end_date in the future. Show me the count."

### What You're Testing
- Basic COUNT aggregation
- Understanding of NULL in business logic
- OR conditions
- Date comparison

### Expected Solution

```sql
SELECT COUNT(*) AS active_subscriptions
FROM subscriptions
WHERE end_date IS NULL
   OR end_date > '2024-04-15';
```

**Alternative acceptable:**
```sql
SELECT COUNT(*) AS active_subscriptions
FROM subscriptions
WHERE end_date IS NULL
   OR end_date >= '2024-04-16';
```

**Also acceptable (using CURRENT_DATE if they ask):**
```sql
-- If they ask "can I use CURRENT_DATE?"
-- Answer: "Sure, for this exercise treat it as 2024-04-15"
SELECT COUNT(*) AS active_subscriptions
FROM subscriptions
WHERE end_date IS NULL
   OR end_date > CURRENT_DATE;
```

### Common Mistakes to Watch For

❌ **Mistake 1: Only checking for NULL, forgetting future dates**
```sql
WHERE end_date IS NULL  -- Misses subscriptions ending in future!
```
**Probe:** "What if a subscription ends next month—is it active today?"

❌ **Mistake 2: Using = NULL**
```sql
WHERE end_date = NULL  -- WRONG!
```
**Probe:** "How do we check for NULL values?"

❌ **Mistake 3: Using AND instead of OR**
```sql
WHERE end_date IS NULL AND end_date > '2024-04-15'  -- Impossible condition!
```
**Probe:** "Can end_date be both NULL AND greater than a date?"

❌ **Mistake 4: Wrong date comparison (< instead of >)**
```sql
WHERE end_date < '2024-04-15'  -- These are EXPIRED!
```

### Verification Query (Run on Your Laptop)

```python
student_query = """
[paste their SQL]
"""
result = con.execute(student_query).df()
print(f"Active subscriptions: {result['active_subscriptions'][0]}")

# Expected: ~12-15 active subscriptions
```

### Timing Guide

- **Under 2 minutes:** Excellent!
- **2-4 minutes:** Good pace.
- **Over 4 minutes:** Nudge: "Think about what makes a subscription active."

---

## QUESTION 2: MRR Calculation (6-12 minutes)

### The Question

> "Great! Now the VP wants to know: **What's our Monthly Recurring Revenue (MRR) by plan type?** Only include active subscriptions. Show me the plan_type, number of active subscriptions, and total MRR. Sort by MRR descending."

### What You're Testing
- Filtering with WHERE before aggregation
- GROUP BY with aggregation
- Understanding of business metrics (MRR)
- SUM vs COUNT
- Ordering results

### Expected Solution

```sql
SELECT
    plan_type,
    COUNT(*) AS num_subscriptions,
    SUM(monthly_price) AS total_mrr
FROM subscriptions
WHERE end_date IS NULL
   OR end_date > '2024-04-15'
GROUP BY plan_type
ORDER BY total_mrr DESC;
```

**Key points:**
- Filter for active subscriptions in WHERE clause (same logic as Q1)
- GROUP BY plan_type to get per-tier metrics
- SUM(monthly_price) calculates MRR
- COUNT(*) works here (no JOINs, so no duplication risk)

### Alternative Acceptable Solutions

**Using CASE to make results more readable:**
```sql
SELECT
    plan_type,
    COUNT(*) AS num_subscriptions,
    SUM(monthly_price) AS total_mrr,
    ROUND(AVG(monthly_price), 2) AS avg_price_per_sub
FROM subscriptions
WHERE end_date IS NULL OR end_date > '2024-04-15'
GROUP BY plan_type
ORDER BY total_mrr DESC;
```
(Adding AVG is extra credit—shows initiative!)

### Common Mistakes to Watch For

❌ **Mistake 1: Forgetting to filter for active subscriptions**
```sql
-- Includes churned subscriptions!
SELECT plan_type, SUM(monthly_price)
FROM subscriptions
GROUP BY plan_type
```
**Probe:** "Should we include subscriptions that ended last year?"

❌ **Mistake 2: Using HAVING instead of WHERE to filter for active**
```sql
-- Less efficient
GROUP BY plan_type
HAVING end_date IS NULL OR end_date > '2024-04-15'
```
**Note:** This might error because you're aggregating before checking row-level conditions. If it works, mention: "WHERE is more efficient here."

❌ **Mistake 3: Counting instead of summing prices**
```sql
SELECT plan_type, COUNT(monthly_price) AS total_mrr  -- Counts rows, not revenue!
```
**Probe:** "Is MRR a count or a dollar amount?"

❌ **Mistake 4: Missing GROUP BY**
```sql
SELECT plan_type, SUM(monthly_price) FROM subscriptions  -- Error!
```
**Probe:** "What happens if you aggregate without GROUP BY?"

### Follow-Up Probes (Choose 1 if time allows)

**If they finish correctly:**
1. "What would happen if monthly_price had NULL values?"
   - Expected: "SUM would ignore them, which might undercount MRR. We'd want to investigate why price is NULL."

2. "How would you calculate *annual* recurring revenue (ARR)?"
   - Expected: "Multiply monthly_price by 12: SUM(monthly_price * 12)"

### Verification Query (Run on Your Laptop)

```python
student_query = """
[paste their SQL]
"""
result = con.execute(student_query).df()
print(result)

# Expected: 3 rows (starter, professional, enterprise)
# MRR values should be in thousands (e.g., $5K-20K)
```

### Timing Guide

- **Under 4 minutes:** Excellent!
- **4-6 minutes:** Good pace.
- **Over 6 minutes:** Nudge: "What do you need to filter for? What do you need to group by?"

---

## QUESTION 3: Inactive Users (12-19 minutes)

### The Question

> "Excellent! Now for user engagement. The customer success team wants to re-engage users who haven't logged in recently. Find all users who **haven't logged in for 30 or more days** (as of April 15, 2024). Show me the user_id, email, company_id, and last_login date. Sort by last_login ascending (oldest first)."

### What You're Testing
- Date arithmetic (days between dates)
- Business logic with date comparisons
- Understanding of "current date" concept
- Sorting by dates

### Expected Solution

**Approach 1: Direct date subtraction**
```sql
SELECT
    user_id,
    email,
    company_id,
    last_login
FROM users
WHERE last_login <= '2024-03-16'
  OR last_login IS NULL
ORDER BY last_login ASC;
```

**Note:** 30 days before April 15 is March 16. Students might calculate this mentally or on the side.

**Approach 2: Using DATE_DIFF or DATEDIFF (more explicit)**
```sql
-- DuckDB syntax
SELECT
    user_id,
    email,
    company_id,
    last_login
FROM users
WHERE DATEDIFF('day', last_login, DATE '2024-04-15') >= 30
   OR last_login IS NULL
ORDER BY last_login ASC;
```

**Both are correct!** The first is simpler; the second shows understanding of date functions.

### Common Mistakes to Watch For

❌ **Mistake 1: Wrong date math direction**
```sql
WHERE last_login >= '2024-03-16'  -- This gets RECENT logins!
```
**Probe:** "If someone logged in on March 16, how many days ago was that from April 15?"

❌ **Mistake 2: Forgetting NULL last_login**
```sql
WHERE last_login <= '2024-03-16'  -- Misses users who NEVER logged in!
```
**Probe:** "What about users who haven't logged in at all? What's their last_login value?"

❌ **Mistake 3: Off-by-one error (using 31 instead of 30, or March 15 instead of 16)**
- This is minor—don't penalize heavily. Say: "Close! Let's verify the math: April 15 minus 30 days is...?"

❌ **Mistake 4: Using wrong date function syntax**
```sql
DATEDIFF(last_login, '2024-04-15')  -- Missing 'day' parameter in DuckDB
```
**Say:** "DuckDB's DATEDIFF needs the unit first: DATEDIFF('day', start_date, end_date)"

### Follow-Up Probes

**If they finish correctly:**
"Good! How would you modify this to find users who logged in YESTERDAY (April 14)?"
- Expected: `WHERE last_login = '2024-04-14'`

**If they included NULL last_login:**
"Great! Why did you check for NULL?"
- Expected: "Users who never logged in are technically inactive, so we should include them."

**If they forgot NULL:**
"What about users who have never logged in?"

### Verification Query (Run on Your Laptop)

```python
student_query = """
[paste their SQL]
"""
result = con.execute(student_query).df()
print(f"Found {len(result)} inactive users")
print(result.head(10))

# Expected: 8-12 users
# Dates should be before March 16, 2024 or NULL
```

### Timing Guide

- **Under 5 minutes:** Excellent date handling!
- **5-7 minutes:** Good pace.
- **Over 7 minutes:** Nudge: "How many days are between March 16 and April 15?"

---

## QUESTION 4: Window Functions - Top Users Per Plan (19-24 minutes)

### The Question

> "Last question! Our product team wants to spotlight power users. Find the **top 3 users by feature usage in each subscription plan tier**. For each user, show their user_id, company_id, plan_type, and total usage count across all features. Rank them within each plan tier."
>
> **Hint:** You'll need to join users → subscriptions, aggregate feature_usage, and use a window function to rank within each plan_type."

### What You're Testing
- Multi-table JOINs
- Aggregation with GROUP BY
- Window functions: ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ...)
- CTEs for readability
- Filtering on window function results

### Expected Solution

```sql
WITH user_feature_totals AS (
    -- Step 1: Calculate total feature usage per user
    SELECT
        u.user_id,
        u.company_id,
        s.plan_type,
        SUM(f.usage_count) AS total_usage
    FROM users u
    INNER JOIN subscriptions s ON u.company_id = s.company_id
    INNER JOIN feature_usage f ON u.user_id = f.user_id
    WHERE s.end_date IS NULL OR s.end_date > '2024-04-15'
    GROUP BY u.user_id, u.company_id, s.plan_type
),
ranked_users AS (
    -- Step 2: Rank users within each plan tier
    SELECT
        user_id,
        company_id,
        plan_type,
        total_usage,
        ROW_NUMBER() OVER (
            PARTITION BY plan_type
            ORDER BY total_usage DESC
        ) AS rank_in_plan
    FROM user_feature_totals
)
-- Step 3: Filter to top 3 per plan
SELECT
    user_id,
    company_id,
    plan_type,
    total_usage,
    rank_in_plan
FROM ranked_users
WHERE rank_in_plan <= 3
ORDER BY plan_type, rank_in_plan;
```

**Key techniques:**
- **CTE 1:** Join three tables and aggregate to user level
- **CTE 2:** Apply ROW_NUMBER() with PARTITION BY plan_type
- **Final query:** Filter for rank <= 3

### Alternative Acceptable Solutions

**Without CTEs (harder to read, but valid):**
```sql
SELECT *
FROM (
    SELECT
        u.user_id,
        u.company_id,
        s.plan_type,
        SUM(f.usage_count) AS total_usage,
        ROW_NUMBER() OVER (
            PARTITION BY s.plan_type
            ORDER BY SUM(f.usage_count) DESC
        ) AS rank_in_plan
    FROM users u
    INNER JOIN subscriptions s ON u.company_id = s.company_id
    INNER JOIN feature_usage f ON u.user_id = f.user_id
    WHERE s.end_date IS NULL OR s.end_date > '2024-04-15'
    GROUP BY u.user_id, u.company_id, s.plan_type
) ranked
WHERE rank_in_plan <= 3
ORDER BY plan_type, rank_in_plan;
```

### Common Mistakes to Watch For

❌ **Mistake 1: Forgetting to filter for active subscriptions**
```sql
-- Includes churned customers!
INNER JOIN subscriptions s ON u.company_id = s.company_id
-- Missing WHERE s.end_date IS NULL OR ...
```
**Probe:** "Should we include usage from companies that canceled their subscription?"

❌ **Mistake 2: Using RANK() or DENSE_RANK() instead of ROW_NUMBER()**
- These can give ties (e.g., two users ranked #1). ROW_NUMBER() guarantees exactly 3 per tier.
- **Say:** "That works, but you might get more than 3 users per tier if there are ties. ROW_NUMBER() ensures exactly 3."

❌ **Mistake 3: Partitioning by wrong column**
```sql
PARTITION BY company_id  -- Wrong! We want per plan_type, not per company
```
**Probe:** "What are we trying to rank within? Companies or plan tiers?"

❌ **Mistake 4: Forgetting GROUP BY before window function**
```sql
-- Missing aggregation step
SELECT ..., ROW_NUMBER() OVER (...)
FROM users u
JOIN feature_usage f ON u.user_id = f.user_id
```
**Probe:** "How do you get total usage per user?"

❌ **Mistake 5: Trying to filter window function in WHERE clause**
```sql
WHERE ROW_NUMBER() ... <= 3  -- Error! Can't use window functions in WHERE
```
**Say:** "Window functions can't go in WHERE. You need a subquery or CTE, then filter in the outer query."

### Follow-Up Probes

**If they finish correctly:**
"Excellent! What would change if we wanted top 5 instead of top 3?"
- Expected: "Change WHERE rank_in_plan <= 3 to <= 5"

"Why did we use ROW_NUMBER instead of COUNT?"
- Expected: "ROW_NUMBER ranks rows. COUNT aggregates. We need ranking here."

**If they struggle:**
- Prompt: "Break it down: First, what do you need to calculate? Then, how do you rank?"

### Verification Query (Run on Your Laptop)

```python
student_query = """
[paste their SQL]
"""
result = con.execute(student_query).df()
print(f"Returned {len(result)} users")
print(result)

# Expected: 9 rows (3 users × 3 plan types)
# Each plan_type should have ranks 1, 2, 3
```

### Timing Guide

- **Under 5 minutes:** Exceptional! This is hard.
- **5-7 minutes:** Excellent pace.
- **Over 7 minutes:** Normal for complexity. Nudge: "Think about CTEs—what's step 1, step 2?"

---

## SCORING RUBRIC

Use this to evaluate overall performance.

### Technical Correctness (40 points)

| Question | Points | Criteria |
|----------|--------|----------|
| Q1 | 8 pts | Correct COUNT, NULL handling, OR logic for active subscriptions |
| Q2 | 10 pts | Correct filtering, GROUP BY, SUM for MRR |
| Q3 | 10 pts | Correct date math, includes NULL last_login |
| Q4 | 12 pts | Multi-table JOIN, aggregation, window function with PARTITION BY, correct filtering |

**Deductions:**
- Syntax errors: -2 pts per query
- Wrong logic but shows understanding: -1 to -2 pts
- Critical conceptual error (e.g., = NULL, wrong window function): -3 pts

### SQL Best Practices (20 points)

- **Readability (8 pts):** Formatting, clear aliases, logical structure
- **Efficiency awareness (6 pts):** WHERE before HAVING, appropriate aggregation
- **NULL handling (6 pts):** Correctly uses IS NULL, considers NULL in business logic

### Communication & Process (25 points)

- **Thinking out loud (10 pts):** Explains approach, walks through logic
- **Asks clarifying questions (8 pts):** Confirms understanding, asks about edge cases
- **Handles feedback (7 pts):** Responds well to probes, adjusts when nudged

### Data & Business Thinking (15 points)

- **Understanding business context (8 pts):** Gets MRR concept, knows what "active" means
- **Edge case awareness (7 pts):** Considers NULL values, date boundaries, ties in ranking

### Total: 100 points

**Scoring bands:**
- **85-100:** Exceptional - ready for FAANG
- **70-84:** Strong - solid understanding
- **55-69:** Competent - needs more practice
- **Below 55:** Needs review - revisit fundamentals

---

## POST-INTERVIEW: Providing Feedback

### What to Say

**If they did well (70+):**
> "Great work! Your understanding of [date math / window functions / business logic] was strong. Especially impressed by [specific thing]. One area to keep practicing: [pick 1]. You're ready for real technical interviews!"

**If they struggled (55-69):**
> "You've got the fundamentals down. I'd recommend practicing [window functions / multi-table JOINs / date calculations]. The way you handled [positive note] was good. Keep practicing these patterns and you'll be ready!"

**If they really struggled (<55):**
> "I can see you understand the basics. Before interviews, review [specific topics]. Focus on [1-2 areas]. Come to office hours—we can work through these together. The fact that you're practicing now is great!"

### Always End Positively

- "These simulations are tough—you did great showing up and trying!"
- "Each time you practice, you get stronger. Keep it up!"
- "You're building skills most candidates don't have. Keep going!"

---

## QUICK REFERENCE: Key Concepts

### Critical Patterns
- ✅ Active subscriptions: `end_date IS NULL OR end_date > CURRENT_DATE`
- ✅ Date math: Understand subtraction and DATEDIFF
- ✅ Window functions: `ROW_NUMBER() OVER (PARTITION BY x ORDER BY y)`
- ✅ NULL handling: Always consider NULL in date/string fields

### Green Flags
- Asks about "today's date" for calculations
- Mentions NULL handling without prompting
- Uses CTEs for complex queries
- Explains business logic (e.g., "MRR is monthly recurring revenue")

### Red Flags
- Uses = NULL
- Forgets to filter for active subscriptions
- Can't explain PARTITION BY
- Silent—doesn't communicate reasoning

---

## APPENDIX: Quick Verification Queries

### Check: How many active subscriptions?
```python
con.execute("""
    SELECT COUNT(*) FROM subscriptions
    WHERE end_date IS NULL OR end_date > '2024-04-15'
""").df()
```

### Check: MRR by plan
```python
con.execute("""
    SELECT plan_type, SUM(monthly_price) AS mrr
    FROM subscriptions
    WHERE end_date IS NULL OR end_date > '2024-04-15'
    GROUP BY plan_type
""").df()
```

### Check: Inactive users
```python
con.execute("""
    SELECT COUNT(*) FROM users
    WHERE last_login <= '2024-03-16' OR last_login IS NULL
""").df()
```

---

## End of Interviewer Guide

**Remember:** This is harder than Scenario 1! It's OK if students struggle with Q4. The goal is learning, not perfection.

Good luck! 🚀
