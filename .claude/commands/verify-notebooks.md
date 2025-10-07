# Verify Notebooks - Pedantic Cell-by-Cell Quality Check

You are tasked with performing **exhaustive cell-by-cell verification** of Jupyter notebooks to ensure teaching quality.

## Your Mission

For each notebook specified (or ALL teaching notebooks if none specified):

1. **Launch parallel verification agents** - one agent per notebook for speed
2. **Each agent must verify EVERY code cell** in their assigned notebook
3. **Report findings** in a structured format
4. **Identify ALL issues** (no matter how minor)
5. **Fix issues found** (if requested)
6. **Re-execute notebooks** to verify fixes work

---

## What to Verify (Per Cell)

For EVERY code cell, check:

### 1. Markdown-Code Alignment
- Does the markdown immediately before the cell accurately describe what the code does?
- Are there promises made that the code doesn't fulfill?
- Are there discrepancies in numbers (e.g., markdown says "5 rows" but LIMIT 10)?

### 2. Output Accuracy
- Does the output (already in notebook) match what markdown promised?
- Are there **empty results** (empty DataFrames) that would confuse students?
- Do calculated values make sense given the data?

### 3. Business Logic Correctness
- Do filter conditions (WHERE clauses) match data constraints?
- Do business questions align with query implementation?
- Are aggregations calculating what they claim to calculate?

### 4. NULL Handling
- Are NULL checks present where needed?
- Do queries handle missing data appropriately?
- Are IS NULL vs = NULL used correctly?

### 5. Pedagogical Soundness
- Do examples teach what they claim to teach?
- Are comparisons (e.g., WHERE vs HAVING) effective?
- Would students understand the output?

### 6. Terminology Consistency
- Is terminology consistent throughout the notebook?
- Do labels match what's being calculated?
- Are business terms used correctly?

---

## Notebooks to Verify

### Teaching Notebooks (highest priority)
```
notebooks/day1_block_a_tidy_foundations.ipynb
notebooks/day1_block_b_01_sql_foundations.ipynb
notebooks/day1_block_b_02_aggregations.ipynb
notebooks/day1_block_b_03_window_functions.ipynb
```

### Exercise Notebooks (verify but don't fix student sections)
```
notebooks/day1_exercise_tidy.ipynb
```

### Assignment Notebooks (if they exist)
```
assignments/hw1/hw1_starter.ipynb
```

---

## Output Format

For each notebook, produce a report:

```markdown
## Cell-by-Cell Verification Report: [notebook_name]

### Cell [N]: [Brief description]
**Markdown says:** [What the markdown promises]
**Code does:** [What the code actually does]
**Output shows:** [What appears in the output]
**Status:** ✅ MATCH / ⚠️ MISMATCH / ❌ ERROR
**Issue (if any):** [Describe discrepancy]

[Repeat for EVERY code cell]

---

## Summary

**Total cells checked:** [N]
**Cells with perfect match:** [N]
**Cells with issues:** [N]

### Issues Found:
1. **[Severity] Cell [N]**: [Brief description]
2. **[Severity] Cell [N]**: [Brief description]

**Severity levels:**
- 🟥 CRITICAL: Empty results, wrong calculations, broken examples
- 🟨 MODERATE: Misleading labels, conceptual mismatches
- 🟦 MINOR: Terminology inconsistencies, wording issues
```

---

## Execution Workflow

1. **Identify notebooks to verify**
   - If user specified paths, use those
   - Otherwise, verify ALL teaching notebooks

2. **Launch parallel agents** (one per notebook)
   ```
   Use Task tool with subagent_type='general-purpose'
   One task per notebook for maximum speed
   ```

3. **Wait for all reports** to complete

4. **Synthesize findings**
   - Total cells verified across all notebooks
   - Total issues found
   - Breakdown by severity
   - Breakdown by issue type (empty results, mismatches, terminology, etc.)

5. **Ask user** if they want issues fixed
   - If YES: Fix all issues using NotebookEdit
   - Re-execute notebooks with jupyter nbconvert
   - Verify fixes work
   - Show before/after for each fix

6. **Offer to commit** changes if fixes were made
   - Generate comprehensive commit message
   - Include issue counts and verification stats
   - Push to GitHub if approved

---

## Example Usage

### Verify All Notebooks
```
/verify-notebooks
```

### Verify Specific Notebook
```
/verify-notebooks notebooks/day1_block_b_02_aggregations.ipynb
```

### Verify and Auto-Fix
```
/verify-notebooks --fix
```

---

## Critical Reminders

### Data Constraints
ALWAYS check actual data constraints before validating queries:
```python
con.execute("SELECT MAX(price) FROM data").df()  # Don't assume max price!
con.execute("SELECT DISTINCT item FROM data").df()  # Check what items exist!
```

### Empty Results = Red Flag
If ANY teaching example returns empty results (0 rows), this is **CRITICAL**:
- Students will think they made a mistake
- Teaching point is lost
- Must be fixed immediately

### Markdown Must Match Code EXACTLY
- If markdown says "first 5 rows", code must use LIMIT 5
- If markdown says "Coffee sales", code must filter Item = 'Coffee'
- If markdown says "revenue", code must calculate price × quantity
- Be pedantic - exact matches only!

---

## Success Criteria

You've succeeded when:

✅ Every code cell in every notebook has been verified
✅ Markdown descriptions match code behavior exactly
✅ All outputs are meaningful (no confusing empty results)
✅ All issues documented with severity levels
✅ Fixes applied (if requested) and verified working
✅ Teaching quality is production-ready

---

**Remember:** This is about **teaching quality**. Students trust that examples work. Every empty result or mismatch erodes that trust. Be thorough, be pedantic, be rigorous.
