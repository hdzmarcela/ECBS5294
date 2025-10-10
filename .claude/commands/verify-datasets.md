---
description: Comprehensive verification of course datasets for pedagogical soundness and technical correctness
---

# Dataset Verification Command

You are verifying datasets for **ECBS5294: Introduction to Data Science: Working with Data**.

**CRITICAL PRINCIPLE:** This verification must be **ADAPTIVE** and **GOAL-ORIENTED**, not hardcoded to specific implementation details.

Focus on: **"Can this dataset achieve the syllabus learning objectives?"**
Not: **"Does this match my expectations of what Day 2 should look like?"**

---

## Command Usage

The user will invoke this command with:
- `/verify-datasets` - Verify all days
- `/verify-datasets 1` - Verify only Day 1
- `/verify-datasets 2` - Verify only Day 2
- `/verify-datasets 3` - Verify only Day 3

---

## Your Verification Process

### Phase 1: Parse Learning Objectives (REQUIRED FIRST STEP)

**Read `syllabus.md`** and extract learning objectives for the requested day(s).

**Day 1 Block A - Expected Learning:**
- Tidy data principles
- UID/Primary key identification
- Type handling (dates, floats, booleans)
- Missing values management
- Transforming messy → tidy

**Day 1 Block B - Expected Learning:**
- Single-table SQL (SELECT, WHERE, ORDER BY, GROUP BY/HAVING)
- NULL behavior
- Window functions: ROW_NUMBER(), LAG(), moving averages
- Understanding windows preserve rows vs GROUP BY collapses

**Day 2 Block A - Expected Learning:**
- INNER/LEFT/RIGHT/FULL JOINs
- Primary key / Foreign key relationships
- ERD understanding
- Join patterns (anti-join, semi-join)
- Duplicate inflation awareness
- Grouping after joins

**Day 2 Block B - Expected Learning:**
- JSON parsing (file or endpoint)
- Nested structure normalization (dict/list)
- Flattening nested objects
- Exploding nested arrays
- Persisting to DuckDB
- Basic typing (dates, etc.)

**Day 3 Block A - Expected Learning:**
- Data quality issues (CSV traps, date handling, categoricals)
- Pipeline patterns: bronze → silver → gold
- Idempotent transforms
- Validations as code (PK unique, required non-nulls, date windows)

**Day 3 Block B:**
- In-class exam (no dataset needed)

---

### Phase 2: File System Checks (Universal)

Run these checks for data/day{N}/ directory:

```
✅ Directory exists
✅ README.md exists and has substantial content (min 100 lines)
✅ Expected files present (inferred from README)
✅ No files > 100MB (git hard limit)
⚠️  Flag files > 50MB (git warning threshold)
✅ No unencrypted solution files (*_solution.ipynb, *_solution.py)
✅ All documented files actually exist
✅ All files tracked in git
```

---

### Phase 3: Documentation Completeness (Universal)

Check README.md contains:

```
✅ Dataset source and URL
✅ License information explicitly stated
✅ License allows educational use (verify for known licenses)
✅ Attribution with proper format (as required by license)
✅ Dataset description (what it represents)
✅ Column/field documentation (schema defined)
✅ Sample code/queries (at least 2 examples)
✅ Learning objectives explicitly listed
✅ Connection to syllabus topics mentioned
✅ "Intentional data characteristics" or similar section
✅ Code blocks properly formatted (```python, ```sql)
✅ File paths are relative (no /Users/, no C:\, no absolute paths)
```

---

### Phase 4: Goal-Oriented Pedagogical Checks (ADAPTIVE!)

**This is the most important phase. You must check if the dataset ACHIEVES the learning objectives, not if it matches a specific implementation.**

#### For Day 1 Block A (Tidy Data Teaching)

**Objective from syllabus:** "Load a messy CSV → tidy → designate UID → one summary table"

**Adaptive checks:**
```python
✅ Dataset has documented "messiness" (README mentions data quality issues)
✅ Types of messiness documented (what students encounter)
✅ "What clean looks like" is defined (success criteria stated)
✅ Primary key is identifiable or can be constructed
✅ At least ONE tidy principle demonstrable:
   - Missing values (multiple representations)
   - Type inconsistencies
   - Structural issues
   - Duplicate rows
   - Unnormalized structure

Assessment: ✅ PASS if cleaning practice is possible and success criteria defined
           ❌ FAIL if dataset is already tidy with no teaching value
           ❌ FAIL if "clean" criteria not documented
```

#### For Day 1 Block B (SQL + Window Functions)

**Objective from syllabus:** "Single-table SQL + window functions (ROW_NUMBER, LAG, moving avg)"

**Adaptive checks:**
```python
✅ Dataset has temporal/sequential dimension (dates, timestamps, ordering)
✅ Dataset has groups/IDs (for PARTITION BY teaching)
✅ Row count > 100 (meaningful for aggregation)
✅ Sample queries in README demonstrate:
   - Basic SELECT/WHERE/GROUP BY
   - At least ONE window function example
✅ Data loads in DuckDB without errors
✅ Can demonstrate "windows preserve rows" vs "GROUP BY collapses"

Assessment: ✅ PASS if window functions are demonstrable with this data
           ❌ FAIL if no temporal/sequential dimension exists
           ❌ FAIL if dataset too small for meaningful aggregation
```

#### For Day 2 Block A (JOIN Teaching)

**Objective from syllabus:** "INNER/LEFT/RIGHT/FULL joins; PK/FK; join patterns"

**Adaptive checks (IMPORTANT - Be Flexible!):**
```python
✅ Multiple related tables exist (at least 2, preferably 3+)
✅ PK/FK relationships documented in README
✅ Can demonstrate INNER JOIN?
   → Check: Matching rows exist between tables

✅ Can demonstrate LEFT JOIN?
   → Check: Unmatched rows exist (rows in left without match in right)
   → OR: README documents alternative teaching approach

✅ Can demonstrate RIGHT JOIN?
   → Check: Unmatched rows exist (rows in right without match in left)
   → OR: README documents "taught conceptually" with explanation
   → NOTE: RIGHT JOIN is rarely used in industry, conceptual teaching is acceptable

✅ Can demonstrate FULL OUTER JOIN?
   → Check: Unmatched rows on both sides OR combination approach

✅ One-to-many relationship exists (for row inflation teaching)
✅ README shows sample JOIN queries
✅ ER diagram or relationship description present

Assessment: ✅ PASS if all four join types achievable (directly OR conceptually)
           ⚠️  WARN if some joins only conceptual but approach is documented
           ❌ FAIL if cannot teach required joins AND no documented strategy
           ❌ FAIL if no PK/FK relationships documented
```

**CRITICAL FOR RIGHT JOIN:** If dataset has no unmatched rows for RIGHT JOIN:
- Check README for documented teaching strategy
- Check for note about industry practices (RIGHT JOIN rarely used)
- If documented, this is **pedagogically acceptable**

#### For Day 2 Block B (JSON Normalization)

**Objective from syllabus:** "JSON → dict/list; normalization; persist to DuckDB"

**Adaptive checks:**
```python
✅ JSON file exists and parses without errors
✅ Has nested structure - at least ONE of:
   - Nested object (dict within dict) for flattening
   - Nested array of objects for exploding (one-to-many)
   - Array of simple values for bridge table (many-to-many)
✅ Normalization opportunities documented
✅ Sample code shows:
   - JSON loading
   - Structure inspection
   - Flattening OR table creation
   - DuckDB persistence
✅ At least one one-to-many relationship demonstrable
✅ Primary key generation shown (if needed for child tables)

Assessment: ✅ PASS if JSON requires normalization to become relational
           ❌ FAIL if JSON is already flat (no teaching value)
           ❌ FAIL if no nested structures present
```

#### For Day 3 Block A (Pipeline Teaching)

**Objective from syllabus:** "Bronze → silver → gold; validations as code"

**Adaptive checks:**
```python
✅ Multiple file formats OR multiple sources
✅ Data quality issues present (for validation teaching)
✅ README documents pipeline stages
✅ Validation examples shown (PK unique, non-nulls, date range, etc.)
✅ Sample code demonstrates idempotent transforms
✅ Bronze/Silver/Gold pattern explained

Assessment: ✅ PASS if multi-stage pipeline is demonstrable
           ❌ FAIL if only single clean file (no pipeline needed)
```

---

### Phase 5: Technical Verification (Universal)

**Load and validate all datasets:**

**For CSV files:**
```python
For each CSV in data/day{N}/:
  ✅ Loads with pandas without errors
  ✅ Loads with DuckDB without errors
  ✅ Row count within ±10% of documented count (if documented)
  ✅ Column names match documentation
  ✅ No completely empty files (0 rows)
  ✅ Primary keys unique (if documented as PK)
  ✅ No entirely NULL columns (unless documented)
```

**For JSON files:**
```python
For each JSON in data/day{N}/:
  ✅ Parses without JSON syntax errors
  ✅ Top-level structure matches documentation
  ✅ Nested structures present (if documented)
  ✅ Row/record count within ±10% of documented
```

**For Parquet files:**
```python
For each Parquet in data/day{N}/:
  ✅ Loads with pyarrow or DuckDB
  ✅ Schema readable
  ✅ Row count reasonable
```

---

### Phase 6: Code Sample Validation

**Extract all code blocks from README and test:**

**For SQL code blocks:**
```python
For each SQL query in README:
  1. Extract the query
  2. Replace table references with actual file paths (relative)
  3. Run in DuckDB
  4. Verify:
     ✅ Query runs without errors
     ✅ Query returns results (unless documented as showing empty case)
     ✅ No absolute paths in query
```

**For Python code blocks:**
```python
For each Python script in README:
  1. Extract the code
  2. Run in isolated environment
  3. Verify:
     ✅ Code runs without errors
     ✅ Imports are standard (pandas, json, duckdb, requests)
     ✅ No absolute paths
     ✅ Relative paths resolve correctly
```

---

### Phase 7: Cross-Reference Validation

**Verify documentation matches reality:**

```python
✅ Documented row counts match actual (±10% tolerance)
✅ Documented column names match actual schema
✅ Example data values in README actually exist in dataset
✅ Sample queries reference actual table/column names
✅ Learning objectives in README align with syllabus objectives
✅ File paths in documentation point to existing files
```

---

## Output Format

**Generate a comprehensive report using this structure:**

```
═══════════════════════════════════════════════════════════
[✅ or ❌] Day {N} Dataset Verification: [PASSED or ISSUES FOUND]
═══════════════════════════════════════════════════════════

📚 Syllabus Learning Objectives (Day {N})
  Block A: [objectives from syllabus]
  Block B: [objectives from syllabus]

📁 File System ({X}/{Y} checks)
  [List each check with ✅/❌/⚠️]
  [If failures, explain what's missing]

📖 Documentation ({X}/{Y} checks)
  [List each check with ✅/❌/⚠️]
  [Note any missing sections]

🎓 Pedagogical Soundness - Block A
  [For each learning objective:]
  [Check if dataset achieves it]
  [If not directly, check if alternative approach documented]

  Assessment: [ACHIEVES or CANNOT ACHIEVE] syllabus objectives
  [Explanation of decision]

🎓 Pedagogical Soundness - Block B
  [Same structure as Block A]

🔬 Technical Verification ({X}/{Y} checks)
  [List each technical check]
  [Note any loading errors or mismatches]

💻 Code Samples ({X}/{Y} tested)
  [Report on each code block tested]
  [Note any failures with error messages]

📊 Data Quality ({X}/{Y} checks)
  [Cross-reference checks]
  [Note any inconsistencies]

═══════════════════════════════════════════════════════════
RESULT: {X}/{Y} checks passed ({Z} warnings, {W} failures)

[✅ or ❌] VERDICT: Dataset is [or is NOT] pedagogically sound and ready for teaching

[If failures:]
CRITICAL ISSUES TO FIX:
1. [Issue with explanation of impact on teaching]
2. [Issue with suggestion for fix]
...

[If warnings:]
NOTES:
- [Explanation of each warning]
- [Why it's acceptable or should be addressed]

Next steps: [What should be done, if anything]
═══════════════════════════════════════════════════════════
```

---

## Key Reminders

1. **Be Adaptive:** Different datasets for same objective should both pass
2. **Check Goals, Not Implementation:** Focus on "can we teach this?" not "does it match exactly?"
3. **Accept Documented Alternatives:** If README explains pedagogical approach, that counts
4. **Industry Context Matters:** Some patterns (like RIGHT JOIN) being rare is pedagogically relevant
5. **Be Thorough:** Check everything systematically
6. **Be Clear:** Explain WHY something passes or fails
7. **Link to Syllabus:** Every failure should reference what objective can't be achieved

---

## Special Cases

**RIGHT JOIN Teaching:**
- If no unmatched rows for RIGHT JOIN examples
- Check if README documents "taught conceptually"
- Check if README mentions industry practice (rarely used)
- If well-documented, this is ✅ PASS with ⚠️ NOTE

**Messy Data:**
- For tidy data teaching, messiness is REQUIRED
- But must be documented with "what clean looks like"

**Large Files:**
- Files 50-100MB: ⚠️ WARN (GitHub will warn but allow)
- Files > 100MB: ❌ FAIL (GitHub hard limit)

**Missing Sections:**
- If section is in syllabus but not in README: ❌ FAIL
- If section is pedagogically important: ❌ FAIL
- If section is minor: ⚠️ WARN

---

Now run the verification for the requested day(s) and generate the comprehensive report.
