# ECBS5294: Introduction to Data Science: Working with Data

**Central European University**

Welcome! This repository contains everything you need for this course: teaching materials, datasets, exercises, assignments, and resources for learning practical data skills.

---

## 📚 What This Course Is About

Real data is messy. Real questions require SQL. Real work needs reproducible pipelines.

In this course, you'll learn the **day-one skills** that analysts and data scientists use every day:

- **Tidy data principles** – structuring data for analysis
- **SQL with DuckDB** – querying, aggregating, joining, and window functions
- **JSON/API ingestion** – turning messy nested data into clean tables
- **Multi-stage pipelines** – bronze → silver → gold patterns
- **Validations as code** – proving your data is correct
- **Stakeholder communication** – explaining what you found and why it matters

By the end, you'll handle 500K-row datasets, write production-quality queries, and build reproducible analysis pipelines.

---

## 🗓️ Course Details

**Instructor:** Eduardo Ariño de la Rubia
**Email:** RubiaE@ceu.edu
**WhatsApp:** +34 654 69 13 63
**Office:** Room A104
**Office Hours:** By appointment

**Format:** Three full-day sessions (2 blocks per day)
**Credits:** 1.0 (runs alongside Coding 1 and Data Science 1)

📄 **Full syllabus with dates:** [syllabus.md](syllabus.md)

---

## 🚀 Quick Start

### Before Day 1

1. **Clone this repository:**
   ```bash
   git clone <repo-url>
   cd ECBS5294
   ```

2. **Set up your environment:**
   - Python 3.x
   - JupyterLab or VS Code
   - DuckDB (`pip install duckdb`)
   - Git

3. **Test your setup:**
   ```bash
   jupyter lab notebooks/day1_setup_check.ipynb
   ```

4. **Bring your laptop to every class!**

---

## 📂 Repository Structure

```
ECBS5294/
│
├── data/                    # Teaching datasets (offline, provided)
│   └── day1/                  # Dirty cafe sales data for practice
│
├── notebooks/               # Teaching notebooks and exercises
│   ├── day1_block_a_tidy_foundations.ipynb
│   ├── day1_block_b_01_sql_foundations.ipynb
│   ├── day1_block_b_02_aggregations.ipynb
│   ├── day1_block_b_03_window_functions.ipynb
│   ├── day1_exercise_tidy.ipynb
│   └── day1_setup_check.ipynb
│
├── assignments/             # Homework assignments with instructions
│   └── hw1/                   # SQL single-table + window functions
│
├── solutions/               # Encrypted solution ZIPs (see below!)
│   ├── README.md              # How to use encrypted solutions
│   └── solutions-*.zip        # Password-protected (released after due dates)
│
├── references/              # Quick references and cheat sheets
│   ├── tidy_data_checklist.md
│   ├── sql_quick_reference.md
│   ├── datasets/              # Dataset documentation
│   ├── papers/                # Summaries of key papers
│   └── teaching/              # Teacher notes (for your benefit!)
│
├── scripts/                 # Utility scripts
│   ├── decrypt_solution.py    # Extract encrypted solutions
│   └── encrypt_solutions.py   # (Instructor use)
│
├── syllabus.md              # Full course syllabus with schedule
├── CLAUDE.md                # Repository development guide
└── README.md                # You are here!
```

**Note:** Materials for Day 2 and Day 3 will be added as the course progresses.

---

## 🔐 About Solutions (They're Here, But Locked!)

**Good news:** All solutions are in this repo from day one.
**Smart design:** They're password-protected until after deadlines.

### Why This Approach?

- ✅ No anxiety about "losing" solutions
- ✅ Available immediately after due dates
- ✅ Encourages trying before looking
- ✅ Lets you verify your work once released

### How to Use Solutions

1. **Try the assignment first** – Even partial attempts build understanding
2. **Check Canvas for password release dates** – Posted after deadlines
3. **Decrypt when available:**
   ```bash
   python scripts/decrypt_solution.py solutions/solutions-day1-blockA.zip
   ```
4. **Learn, don't copy** – Type out solutions to build muscle memory

📖 **Full guide:** [solutions/README.md](solutions/README.md)

---

## 📅 Course Overview

### Day 1 – Tidy Data & SQL Foundations
- **Block A:** Tidy data foundations, primary keys, types, missing values
- **Block B:** SQL basics + window functions primer (ROW_NUMBER, LAG, moving averages)
- **Assigned:** Homework 1 (due start of Day 2)

### Day 2 – Joins & JSON Ingestion
- **Block A:** SQL joins & relational modeling (INNER/LEFT/RIGHT/FULL)
- **Block B:** JSON & APIs → tidy tables
- **Assigned:** Homework 2 (due start of Day 3)

### Day 3 – Pipelines & Assessment
- **Block A:** Data in the wild + pipeline patterns (bronze/silver/gold)
- **Block B:** In-class exam (paper/pen, 100 minutes)
- **Assigned:** Homework 3 (due one week after class)

📅 **Specific dates:** See [syllabus.md](syllabus.md) for the current term's schedule.

---

## 📊 Grading

| Component | Weight | What It Tests |
|-----------|--------|---------------|
| **Homework 1** (SQL + windows) | 20% | Query writing, aggregations, window functions |
| **Homework 2** (JSON pipeline) | 25% | Data ingestion, normalization, persistence |
| **Homework 3** (End-to-end) | 25% | Complete pipeline with validation + communication |
| **In-class deliverables** | 5% | Short exercises (completion-based) |
| **In-class exam** (Day 3) | 25% | SQL, joins, data thinking (paper/pen, closed-book) |

**Late policy:** −10% per 24 hours (48-hour max)
**Median target:** B+ (roughly ⅓ of class at A/A-)

---

## 🎯 Key Resources

### Quick References
- [Tidy Data Checklist](references/tidy_data_checklist.md) – Primary keys, types, missing values
- [SQL Quick Reference](references/sql_quick_reference.md) – Syntax cheat sheet

### Textbooks & Docs
- Arthur Turrell, *Coding for Economists* (selected chapters)
- [The Carpentries](https://carpentries.org/) (Unix, Git, Python episodes)
- [DuckDB Documentation](https://duckdb.org/docs/)

### Teaching Materials
- All notebooks in `notebooks/` – worked examples with explanations
- `references/teaching/` – Teacher notes (these show you what's important!)

---

## 💡 Tips for Success

### Reproducibility Is Everything
- ✅ **Restart & Run All** before submitting – If it doesn't run cleanly, you'll lose points
- ✅ **Use relative paths** – `data/file.csv`, not `/Users/yourname/...`
- ✅ **Commit often** – Small, logical commits help you track changes

### Data Thinking Habits
- Always identify and validate your **primary key**
- Handle **NULL values** consciously (they affect everything!)
- Use **assertions as tests** – Prove your data is correct
- **Document your choices** – Why did you handle missing values this way?

### SQL Strategies
- **Start small:** Use `LIMIT 10` while developing queries
- **Build incrementally:** Add one clause at a time
- **Format for readability:** Uppercase keywords, indentation, one clause per line
- **Check for NULLs:** Always consider `IS NULL` / `IS NOT NULL`

### Window Functions Mental Model
- **Windows KEEP row count** (every row gets a value)
- **GROUP BY COLLAPSES rows** (aggregates reduce rows)
- You can't filter on window functions directly – use a subquery!

### When You're Stuck
1. Review teaching notebooks
2. Check the quick references
3. Read error messages carefully
4. Start simpler (remove complexity, then add back)
5. **Ask for help!** Office hours, email, WhatsApp

---

## 🚫 Academic Integrity

### What You CAN Do
✅ Review course materials and documentation
✅ Discuss concepts with classmates (conceptually, not code)
✅ Ask instructor/TA for clarification
✅ Use official documentation (pandas, DuckDB, etc.)

### What You CANNOT Do
❌ Use AI tools (ChatGPT, Claude, Copilot) for graded work
❌ Copy code from classmates
❌ Share your solutions with others
❌ Use solutions from previous years

**Why?** We need to assess YOUR understanding so we can help where you're stuck.

**Policy:** To align with parallel courses (Coding 1, Data Science 1), AI assistants are not permitted for homework or exams. Use them for personal study only.

---

## 🎓 Learning Outcomes

By the end of this course, you will:

1. **Apply tidy data principles** to messy real-world datasets
2. **Write SQL queries** confidently (SELECT, WHERE, JOIN, GROUP BY, window functions)
3. **Ingest JSON/APIs** and normalize into analysis-ready tables
4. **Build reproducible pipelines** with validations as code
5. **Communicate findings** to stakeholders with data dictionaries and clear narratives
6. **Develop performance intuition** for data operations
7. **Handle real data problems** (NULL values, type issues, missing data, duplicate keys)

These are the skills you'll use **on day one** of any analyst or data science role.

---

## 🌟 Philosophy

> **Real data is messy. Embrace it.**

This course doesn't hide the messiness – we work with dirty CSVs, inconsistent types, missing values, and 500K-row datasets because **that's what you'll face in the real world**.

Your job isn't to memorize syntax. It's to:
- **Think clearly** about data structure
- **Make defensible choices** about how to handle issues
- **Document your work** so others (and future you) understand
- **Validate everything** – trust, but verify!

By the end, you'll feel confident tackling real data problems, not just textbook examples.

---

## 📬 Getting Help

**Stuck on something?** Don't suffer in silence!

- **Office hours:** By appointment (Room A104)
- **Email:** RubiaE@ceu.edu
- **WhatsApp:** +34 654 69 13 63
- **In class:** Ask questions! Everyone else probably has the same question.

**Rule of thumb:** If you're stuck for more than 15 minutes, reach out.

---

## 🛠️ Technical Setup

**Required:**
- Python 3.x
- JupyterLab or VS Code
- DuckDB: `pip install duckdb`
- Git

**Recommended:**
- pandas: `pip install pandas`
- numpy: `pip install numpy`

**Test your setup:**
```bash
jupyter lab notebooks/day1_setup_check.ipynb
```

All teaching datasets are **provided offline** in this repo – no downloads needed!

---

## 🎉 Let's Get Started!

This course moves fast, but that's because every minute is practical, hands-on skill-building. By the end of three sessions, you'll have built:

- A cleaned dataset from messy CSV data
- SQL queries on 500K+ row datasets
- A JSON-to-database pipeline
- An end-to-end analysis with validation and stakeholder communication

These are portfolio pieces. These are interview talking points. These are **real skills**.

Ready? Open up `notebooks/day1_setup_check.ipynb` and let's make sure you're ready to go.

**See you in class!** 🚀

---

*Questions about this README or the course? Contact the instructor.*
