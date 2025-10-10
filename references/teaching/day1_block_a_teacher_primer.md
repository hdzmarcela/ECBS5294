# Day 1, Block A: Data Thinking & Tidy Foundations
## Teacher Primer

**Duration:** 90 minutes (13:30–15:10)  
**Audience:** Absolute beginners, first exposure to thinking about data  
**Context:** First day of MSBA program, runs parallel to Coding 1 and Data Science 1

---

## Learning Objectives

By the end of Block A, students will be able to:

1. **Articulate the strategic value** of data structure ("defining the nouns and verbs of the business")
2. **State the three rules** of tidy data and recognize when data violates them
3. **Identify the five common messiness patterns** in real datasets
4. **Designate and validate a primary key (UID)** for a dataset
5. **Recognize common type pitfalls** (dates, floats, strings-as-numbers)
6. **Handle missing values** appropriately (distinguish NULL from other representations)
7. **Transform a messy dataset** into a tidy format with proper keys and types

---

## Session Flow (90 minutes)

### 1. Hook: The Power of Data Structure (10 minutes)

**Opening statement:**
> "When you define how data is structured, you're not just organizing information—you're defining the language your entire organization will use to make decisions."

**Key Teaching Points:**
- Every "customer," "order," "product" in your database becomes a **noun** the business rallies around
- Every "purchase," "return," "review" becomes a **verb** that drives metrics
- You're laying the foundation for how people think, talk, and measure success
- Example: When you decide "what is a customer?" (one per email? per household? per device?), you're making a business decision, not just a technical one

**Historical Context (5 min):**
- Timeline: Filing cabinets → 1960s databases → 1970 Codd revolution
- The problem Codd solved: **"Store each fact once, answer any question"**
- Why students should care: They're learning the technology that solved one of computing's fundamental problems
- Disk space was expensive; redundancy was wasteful; flexibility was limited
- [Reference: `references/papers/database_history.md`]

**Pedagogical Note:** This hooks business students immediately—data isn't just technical, it's strategic. Don't apologize for Excel; celebrate that they know it. Frame this as *expanding* their toolkit.

---

### 2. The Three Rules of Tidy Data (20 minutes)

**Introduce Framework:**
- Hadley Wickham (statistician, created tidyverse in R)
- Published influential paper defining "tidy data" principles
- These rules work across all tools (Python, R, SQL, Excel)

**The Three Rules:**
1. Each variable is a column
2. Each observation is a row
3. Each value is a cell

**Teaching Strategy:**
- Show messy example FIRST (e.g., religion/income table with brackets as columns)
- Ask: "What makes this hard to work with?"
- Then show tidy version
- Walk through each rule: "Does this follow rule 1? Rule 2? Rule 3?"

**Why These Rules Matter:**
- Consistency makes tools easier to learn and use
- Vectorized operations work naturally (add up a column)
- Analysis becomes intuitive (filter rows, group columns)
- Joining data becomes possible (need consistent row-level observations)

**Interactive Moment:**
- Show 2-3 quick examples on screen
- Ask students: "Is this tidy? Why or why not?"
- Build muscle for recognizing structure

**Reference:** `references/papers/tidy_data_summary.md`

---

### 3. The Five Common Problems (15 minutes)

**Frame It:**
> "Tidy datasets are all alike, but every messy dataset is messy in its own way." – Hadley Wickham

**Teaching Approach:**
- Use visual examples for each
- Keep examples business-relevant (sales, customers, transactions)
- Don't dwell on #3 (matrix-style)—it's rare and confusing for beginners

**The Five Problems:**

1. **Column headers are values, not variable names**
   - Bad: `year_2020`, `year_2021`, `year_2022` as separate columns
   - Good: `year` column with values 2020, 2021, 2022
   - Business impact: Can't easily plot trends or add new years

2. **Multiple variables stored in one column**
   - Bad: `male_under_18` combining gender and age
   - Good: `gender` (male) and `age_group` (under_18) as separate columns
   - Business impact: Can't analyze by gender OR age separately

3. **Variables stored in both rows AND columns**
   - Example: Matrix/pivot table style where both axes are variables
   - Mention briefly, skip detailed example (confusing for day 1)

4. **Multiple types of observational units in same table**
   - Bad: Mixing customer info with transaction info in one row (redundant customer data repeated)
   - Good: `customers` table + `transactions` table, linked by `customer_id`
   - Business impact: Redundancy, update anomalies, storage waste

5. **Single observational unit spread across multiple tables**
   - Bad: `sales_jan.csv`, `sales_feb.csv`, `sales_mar.csv`
   - Good: One `sales` table with a `month` column
   - Business impact: Can't easily query across time periods

**Teaching Tip:** Use colorful slide visuals. Draw these on board if possible. Concrete beats abstract.

---

### 4. Primary Keys & Identity (15 minutes)

**Core Concept:**
> "Every entity needs a unique identifier—a primary key (UID). This is the backbone of data integrity."

**What Makes a Good Primary Key:**
- **Unique** - no duplicates (must validate with code!)
- **Non-null** - every row must have one
- **Stable** - doesn't change over time
- **Single-purpose** - exists to identify, not to describe

**Types of Keys:**
- **Natural key:** Something inherent to the entity (email, SSN, ISBN)
- **Surrogate key:** Made up for database purposes (customer_id: 1, 2, 3...)
- **Composite key:** Multiple columns together (store_id + date for daily store sales)

**Why It Matters (Business Framing):**
- Foundation for joining tables (which customer made which purchase?)
- Ensures you can uniquely identify each observation
- Prevents duplicate records (customer entered twice?)
- Essential for updates (which record do I change?)
- Enables tracking over time (same customer, different transactions)

**Red Flags Students Should Learn to Spot:**
- No obvious UID → need to create one or investigate grain
- Multiple rows with same UID → data quality problem, investigate immediately
- UID with NULLs → missing identifiers, data incomplete

**Code Demo:**
```python
# Check if transaction_id is a valid primary key
assert df['transaction_id'].is_unique, "Duplicate transaction IDs found!"
assert df['transaction_id'].notna().all(), "NULL transaction IDs found!"
```

**Teaching Note:** Students often confuse "primary key" with "important column." Emphasize: it's about *identity*, not importance.

---

### 5. Types & Common Pitfalls (10 minutes)

**Frame:**
> "Computers don't understand context—you must tell them what each column means. The wrong type silently breaks calculations."

**Common Type Pitfalls:**

**1. Dates**
- Multiple formats in same column: "2024-10-08", "10/08/2024", "Oct 8, 2024"
- Timezone issues (UTC vs local)
- Excel converting dates to numbers (serial dates)
- **Lesson:** Always parse explicitly with expected format

**2. Floating-Point Precision**
- Demo: `0.1 + 0.2` → `0.30000000000000004` (not exactly 0.3!)
- Why: Binary representation limitations
- Matters for: financial calculations, equality checks (`==` can fail)
- **Solution:** Use Decimal types for money, never compare floats with `==`

**3. Numbers Stored as Strings**
- "$1,234.56" - currency symbols, thousands separators
- "5%" - percentage signs
- "42.5 kg" - units embedded
- Phone numbers with formatting: "(555) 123-4567"
- **Lesson:** Must clean/parse before mathematical operations

**4. Booleans**
- Many representations: True/False, 1/0, "yes"/"no", "Y"/"N", "T"/"F"
- Inconsistent encoding breaks filtering and aggregation
- **Lesson:** Standardize early

**Demo Strategy:**
- Show 2-3 of these failing in Python (live coding)
- Let them see the error messages
- Show the fix
- Normalize that this happens to everyone

**Teaching Note:** Don't overwhelm. Pick the most relevant examples. Dates and string-numbers are most common for MSBA students.

---

### 6. Missing Values (10 minutes)

**Core Concept:**
> "Missing data IS data—but different representations mean different things. Your choice matters."

**Common Representations:**
- `NULL` / `None` / `NaN` (proper missing - database/pandas standard)
- Empty string `""`
- Zero `0`
- Sentinel values: `-999`, `-1`, `"N/A"`, `"Unknown"`, `"ERROR"`, `"#N/A"`

**Why It Matters:**
- `NULL` is **excluded** from aggregations (COUNT, AVG, SUM)
- `0` is **included** in calculations (changes the mean!)
- Empty string `""` is **not** NULL (it's a value: "nothing")

**Example Impact:**
```python
# These give different results!
[10, 20, NULL].average() → 15  # NULL excluded
[10, 20, 0].average() → 10     # 0 included
```

**Decision Framework (Teach This):**
Three different meanings:
1. **"Not applicable"** - this field doesn't apply to this row (e.g., "spouse name" for single person)
2. **"Unknown"** - we don't know the value but it exists (e.g., customer age not collected)
3. **"Not collected yet"** - temporal gap (e.g., survey response pending)

Your representation choice should reflect the meaning. Document it!

**Best Practice:**
- Use `NULL` for true missing
- Avoid sentinel values when possible (hard to remember, easy to forget in analysis)
- Be consistent across columns
- Document your missing value strategy in data dictionary

**Teaching Note:** Students often don't realize empty string ≠ NULL. Demo this explicitly.

---

### 7. In-Class Exercise Setup (10 minutes)

**The Task:**
> "Transform a messy cafe sales dataset into a tidy format, designate a primary key, and create one summary table."

**What Students Will Do:**
1. Load `data/day1/messy_cafe_sales.csv`
2. Explore and identify tidy data violations
3. Identify data quality issues (types, missing values, duplicates)
4. Transform to tidy format (if needed)
5. Create or validate a primary key
6. Handle types correctly (dates, numbers)
7. Handle missing values appropriately
8. Create a summary table (e.g., total sales by payment method)
9. Document assumptions made

**Deliverable:**
- Jupyter notebook that runs "Restart & Run All" successfully
- Clear markdown explanations of choices made

**Support Provided:**
- Starter notebook: `notebooks/day1_exercise_tidy.ipynb` with structured TODOs
- Data dictionary: `data/day1/README.md` describing the dataset

**Time Allocation:**
- 10 minutes: Setup and initial exploration (in class)
- Remainder: Work independently or in pairs
- Can continue as homework if needed (not graded, but strongly encouraged)

**Teaching Strategy:**
- Circulate while students work
- Help with technical issues (imports, paths)
- Ask guiding questions rather than giving answers: "Is this column a variable or a value?" "What makes this a unique identifier?"
- Normalize struggle: "This is hard for everyone at first. That's why we practice."

**Solution Release:**
- Provide `notebooks/day1_exercise_tidy_solution.ipynb` after class or next day
- Annotated with explanations of choices made
- Show that multiple approaches can be valid (if assumptions are documented)

---

## Materials Required

### Created for Teaching:
1. **Teaching notebook:** `notebooks/day1_block_a_tidy_foundations.ipynb`
   - All concepts with executable examples
   - Visual examples from Hadley's paper
   - Database history timeline
   - Type pitfall demonstrations
   - Missing value examples

2. **Slide deck (optional):** For projector/screen during lecture portions
   - PDF or reveal.js slides from Jupyter
   - Visual examples of messy vs tidy
   - The five problems with clear graphics

3. **Teaching examples:** Small embedded datasets in teaching notebook
   - 2-3 tiny examples (10-20 rows) showing each messiness pattern

### Created for Student Exercise:
4. **Exercise dataset:** `data/day1/messy_cafe_sales.csv`
   - Base: Kaggle cafe sales (subset to 500-1000 rows for manageability)
   - Add teaching-specific issues:
     - Multiple date formats mixed
     - Currency symbols in prices ($12.50)
     - Missing values as "", "N/A", NULL
     - Some duplicate transaction IDs (data quality issue to find)
     - Payment methods with inconsistent capitalization
   - Data dictionary in `data/day1/README.md`

5. **Exercise starter:** `notebooks/day1_exercise_tidy.ipynb`
   - Pre-structured sections with TODOs
   - Load and explore
   - Identify issues
   - Transform to tidy
   - Validate primary key
   - Create summary
   - Includes assertion templates for students to complete

6. **Exercise solution:** `notebooks/day1_exercise_tidy_solution.ipynb`
   - Fully worked with explanations
   - Released after class

### Reference Materials:
7. **Quick reference card:** `references/tidy_data_checklist.md`
   - One-page reminder of key concepts
   - Three rules, five problems, validation patterns

---

## Pedagogical Approach for Absolute Beginners

**Core Principles:**

1. **Concrete before abstract**
   - Show examples before stating rules
   - Use familiar business contexts (sales, customers, transactions)
   - Let them see the problem before teaching the solution

2. **Build confidence early**
   - Start with wins (successfully loading data)
   - Normalize mistakes ("Everyone gets this wrong at first")
   - Show that errors are information, not failure

3. **Interleave explanation and practice**
   - Don't lecture for 45 minutes then practice
   - 10-15 minute segments with immediate examples
   - Keep them active and engaged

4. **Make it relevant**
   - Tie every concept to business decisions
   - "When you decide what a customer is, you're making a strategic choice"
   - "Bad data structure costs time and money"

5. **Normalize debugging**
   - Show mistakes and fixes
   - Use assert statements as "checks" not "tests" (less intimidating)
   - Model: "Let me try this... hmm, error... okay, let me fix it..."

6. **Use multiple representations**
   - Visual (tables on screen)
   - Verbal (explanations)
   - Kinesthetic (they code)
   - Appeals to different learning styles

**Common Beginner Struggles to Anticipate:**

| Struggle | Mitigation Strategy |
|----------|-------------------|
| "What even is a primary key?" | Show 5+ concrete examples before defining abstractly |
| "Why does this matter?" | Keep tying back to business decisions and downstream impact |
| Notebook state confusion | Teach "Restart & Run All" in first 10 minutes, make it a habit |
| Path issues | Use relative paths from start, show project structure |
| "My code doesn't work" | Circulate, debug together, model troubleshooting process |
| Overwhelmed by options | Provide starter code with TODOs, clear structure |
| Perfectionism paralysis | "Document your assumptions and move forward—iteration is expected" |

---

## Pacing Guide

| Time | Activity | Mode |
|------|----------|------|
| 0:00-0:10 | Hook: Power of data structure + history | Interactive lecture |
| 0:10-0:30 | Three rules of tidy data + examples | Interactive lecture + Q&A |
| 0:30-0:45 | Five common problems | Visual examples + discussion |
| 0:45-0:60 | Primary keys + types + missing values | Lecture + demos |
| 0:60-0:70 | Exercise setup + initial exploration | Hands-on |
| 0:70-0:90 | Continued work + circulation | Independent work |

**Flexibility Notes:**
- If discussion is rich, let it run (compress later sections)
- If students grasp quickly, move to exercise sooner
- If struggling, add more examples in the moment

---

## Assessment (Formative)

**During Class:**
- Circulate during exercise time
- Observe: Are they loading data? Exploring? Asking good questions?
- Listen for: Proper terminology usage ("this violates tidy rule 1")

**After Class:**
- Review submitted exercise notebooks (not graded, but reviewed)
- Look for: Appropriate use of assertions, documented assumptions, clear thinking
- Common errors inform next class or HW1 design

**Not Assessed:**
- Perfect code (not expected)
- Complete solution in 90 minutes (not expected)
- Prior knowledge (none assumed)

---

## Connection to Later Material

**Immediate (Block B same day):**
- Tidy data makes SQL easier (one row per observation = one row per query result)
- Primary keys become critical for joins
- Types matter for WHERE clauses and aggregations

**Near-term (Day 2-3):**
- Tidy data enables joins (proper grain)
- Primary/foreign key relationships make sense
- JSON normalization produces tidy tables

**Long-term (Rest of program):**
- Foundation for all analytics work
- Data engineering builds on these concepts
- Machine learning requires tidy data

---

## Resources Used

- Hadley Wickham's "Tidy Data" paper (2014) - `references/papers/tidy_data_summary.md`
- R for Data Science Ch. 5 (Data Tidying) - concepts adapted to Python
- Database history - `references/papers/database_history.md`
- Kaggle cafe sales dataset - `references/datasets/kaggle_datasets_for_teaching.md`

---

## Instructor Reminders

**Before Class:**
- [ ] Test all code in teaching notebook (fresh kernel)
- [ ] Verify data files load correctly with relative paths
- [ ] Have solution notebook ready but not distributed
- [ ] Check projector/screen setup

**During Class:**
- [ ] Start with energy—this is their first exposure!
- [ ] Watch the clock but don't rush quality explanations
- [ ] Encourage questions throughout
- [ ] Circulate during exercise time

**After Class:**
- [ ] Release solution notebook
- [ ] Note what worked/didn't for next year
- [ ] Identify students who may need extra support

**Philosophy:**
You're not just teaching technical skills—you're teaching **how to think about data**. The technical skills follow from the thinking. Invest in the conceptual foundation.
