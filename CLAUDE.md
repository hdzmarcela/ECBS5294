# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a course repository for **ECBS5294: Introduction to Data Science: Working with Data** at Central European University. The course focuses on practical data literacy: tidy data principles, SQL with DuckDB, JSON/API ingestion, and reproducible multi-stage pipelines.

## Project Structure

Expected directories:
- `/data` - Teaching datasets (offline, provided)
- `/notebooks` - Jupyter notebooks for exercises and assignments
- `/sql` - SQL query files
- `/scripts` - Utility scripts for course management
- `/solutions` - Encrypted solution archives (password-protected ZIPs)
- `/references` - Teaching resources and documentation
- Root contains `README.md` and course materials

## Solution File Management

**CRITICAL SECURITY REQUIREMENT**: Solution files must NEVER be committed to git unencrypted.

### File Naming Conventions

**Solution Source Files** (before encryption):
- Jupyter notebooks: `{assignment}_solution.ipynb`
- Python scripts: `{assignment}_solution.py`
- SQL queries: `{assignment}_solution.sql`

Examples:
- `day1_exercise_tidy_solution.ipynb`
- `hw1_solution.ipynb`
- `query_solution.sql`

**Encrypted Archives** (for git commits):
- Pattern: `solutions/solutions-{descriptor}.zip`
- Examples:
  - `solutions/solutions-day1-blockA.zip`
  - `solutions/solutions-hw1.zip`
  - `solutions/solutions-midterm.zip`

### Encryption Workflow

**Before ANY git commit containing solutions**:

1. **Encrypt the solution**:
   ```bash
   python scripts/encrypt_solutions.py \
     notebooks/day1_exercise_tidy_solution.ipynb \
     --password "secure-password" \
     --day 1 \
     --block A
   ```

2. **Check solution status**:
   ```bash
   python scripts/list_solutions.py
   ```

3. **Commit ONLY the encrypted ZIP**:
   ```bash
   git add solutions/solutions-day1-blockA.zip
   git commit -m "Add encrypted solutions for Day 1 Block A"
   ```

4. **Document password** in `solutions/PASSWORDS.md` (gitignored):
   - File must never be committed
   - Keep backed up securely outside repository

### Git Pre-Commit Hook

The repository has an **automated pre-commit hook** that:
- ✅ **Allows**: Encrypted ZIP files in `solutions/`
- ✅ **Verifies**: ZIPs are password-protected
- ❌ **Blocks**: Any `*_solution.ipynb` or `*_solution.py` files
- ❌ **Blocks**: Any files with "solution" in path (case-insensitive) except ZIPs

**Install/activate the hook**:
```bash
./scripts/setup_hooks.sh
```

### .gitignore Patterns

The following patterns are gitignored to prevent accidental commits:
```
*_solution.ipynb
*_solution.py
*/solution.ipynb
*/solution.py
solutions/PASSWORDS.md
solutions/decrypted/
solutions/.encryption_log.txt
```

### Available Scripts

- **`scripts/encrypt_solutions.py`** - Create password-protected solution ZIPs
- **`scripts/decrypt_solution.py`** - Extract encrypted solutions (instructor/TA use)
- **`scripts/list_solutions.py`** - Show status of all solutions (encrypted vs unencrypted)
- **`scripts/setup_hooks.sh`** - Install git pre-commit hook

### Security Rules

**NEVER**:
- Commit unencrypted solution files
- Commit `solutions/PASSWORDS.md`
- Use weak or guessable passwords
- Share passwords before assignment due dates
- Disable git hooks without good reason

**ALWAYS**:
- Encrypt solutions before committing
- Test decryption before pushing
- Run `list_solutions.py` before git commits
- Document passwords in `PASSWORDS.md` immediately
- Keep `PASSWORDS.md` backed up securely (outside repo)

### For Students

Students receive encrypted ZIPs from day one but passwords are released only after assignment due dates. This approach:
- Ensures solutions are immediately available post-deadline
- Encourages attempting problems before looking at answers
- Removes anxiety about "losing" solutions

See `solutions/README.md` for student-facing instructions.

## Core Technologies

- **Python 3.x** - Primary language
- **JupyterLab or VS Code** - Development environment
- **DuckDB** - Embedded SQL database (Python API or CLI)
- **Git** - Version control

## Key Concepts & Patterns

### Data Pipeline Pattern (Bronze → Silver → Gold)
- **Bronze**: Raw ingestion (preserve original)
- **Silver**: Cleaned, typed, validated
- **Gold**: Analysis-ready with joins and aggregations

### Tidy Data Principles
- Each variable is a column
- Each observation is a row
- Designate UID/primary keys explicitly
- Handle types correctly (dates, floats, booleans)
- Document missing value handling

### SQL Focus Areas
- Single-table queries: `SELECT`, `WHERE`, `ORDER BY`, `GROUP BY/HAVING`
- Joins: INNER, LEFT, RIGHT, FULL (watch for duplicate inflation)
- Window functions (scoped primer):
  - `ROW_NUMBER()` for deduplication/latest records
  - `LAG()` for period-over-period calculations
  - Moving averages with `ROWS BETWEEN`
- NULL handling in conditions and aggregations

## Development Requirements

### Reproducibility Standards
- All code must **Run-All** successfully from clean clone
- Use **relative paths** only
- No hardcoded absolute paths
- Clear notebook cell execution order
- Small, logical Git commits

### Validation Patterns
Include validations as code:
- Primary key uniqueness checks
- Required field non-null assertions
- Date window/range validations
- Join cardinality checks

### Communication Standards
- Provide concise data dictionaries for outputs
- Include stakeholder-facing notes (8-10 sentences)
- Document assumptions and limitations
- Present results as clear tables/metrics

## Common Tasks

### Working with DuckDB
```python
import duckdb
con = duckdb.connect('database.db')
# Query CSVs directly
con.execute("SELECT * FROM 'data/file.csv'")
# Query Parquet
con.execute("SELECT * FROM 'data/file.parquet'")
```

### JSON Normalization Pattern
1. Ingest JSON (file or endpoint)
2. Parse to dict/list structures
3. Normalize nested structures to flat tables
4. Persist to DuckDB with proper types
5. Join with dimension tables as needed

### Performance Considerations
- Prefer dict lookups over list iteration for key-based access
- Understand join cardinality impact on result size
- Use columnar formats (Parquet) for larger datasets over CSV

## Data Handling Notes

### Common Pitfalls
- Locale-dependent CSV separators
- Floating-point precision issues
- Date parsing and timezone handling
- Header drift in spreadsheets
- Categorical codes vs labels (use reference tables)

### Preferred Approaches
- SQL for set-based operations, filtering, aggregation
- Python for complex transformations, API calls, normalization
- Assertions for data quality checks (fail fast)
- Idempotent transforms (re-runnable without side effects)

## Academic Context

**AI Tool Policy**: AI assistants (ChatGPT/Claude/Copilot) are NOT permitted for graded work. Only assist with learning/understanding, not assignment completion.

**Grading Components**: Correctness (40%), Data thinking (25%), Reproducibility (20%), Communication (15%)
