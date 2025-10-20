# Day 3 Teacher Primer

**ECBS5294: Introduction to Data Science: Working with Data**

---

## Day Overview

**Theme:** Bringing it all together - pipelines, validations, and data survival skills

**Learning Objectives:**
1. Understand bronze → silver → gold pipeline pattern
2. Write data validations as assertions
3. Recognize and handle common data quality issues
4. Build end-to-end data processing workflows

**Materials:**
- `notebooks/day3/day3_block_a_pipelines_and_validations.ipynb` - Teaching notebook
- `notebooks/day3/day3_exercise_mini_pipeline.ipynb` - In-class exercise (15 min, graded)
- `assignments/hw3/` - Take-home end-to-end project
- `assignments/final_exam/` - 60-minute comprehensive exam

---

## Block A: Pipelines & Validations (90 minutes)

### Time Allocation

| Activity | Minutes | Notes |
|----------|---------|-------|
| Why pipelines? | 5 | Business motivation |
| Bronze → Silver → Gold concept | 10 | High-level overview |
| Live example walkthrough | 25 | Olist data, all 3 layers |
| Validations deep dive | 20 | Assertions, fail-fast |
| Data survival tips | 15 | Common issues, practical advice |
| In-class exercise | 15 | Graded micro-pipeline |
| **Total** | **90** | Includes buffer |

### Teaching Tips

**Why Pipelines Matter (5 min):**
- Start with business scenario: "Data analyst gets fired because report was wrong"
- Ask: "How do you know your data is correct?"
- Frame: Pipelines = quality control for data
- Don't dive into technical details yet

**Bronze → Silver → Gold (10 min):**
- Use physical metaphor: "Ore → ingots → coins"
- Bronze = raw material (keep original)
- Silver = refined (clean, validated)
- Gold = finished product (business metrics)
- Key insight: "You can always go back to bronze"

**Live Example (25 min):**
- Walk through Day 3 Block A notebook
- Show each layer on Olist data
- **Critical:** Execute every cell, show outputs
- Point out: "See how row count changes? That's filtered data."
- Emphasize: "Assertions catch problems EARLY"

**Validations Deep Dive (20 min):**
- Start with: "What could go wrong with this data?"
- Students suggest issues (NULLs, duplicates, types)
- Show corresponding assertions
- Demo: Comment out assertion, show pipeline breaking later
- Message: "Fail fast = easier debugging"

**Data Survival Tips (15 min):**
- Share war stories (NULLs, mixed formats, encoding)
- Show real examples from Chicago/NYC data
- Practical fixes students will use
- Don't dwell on edge cases - keep it actionable

**In-Class Exercise (15 min):**
- This is GRADED (5% of course)
- Students build mini bronze → silver → gold pipeline
- 500-row Olist subset (manageable in 15 min)
- Walk around, answer questions
- Don't give answers, give hints
- Collect notebooks at end of class

---

## Common Student Questions

### "Why not just clean data in one step?"

**Answer:**
"Great question! You *can* do it all at once, but what happens if:
- Your boss says 'change the date filter'?
- You find a bug in your revenue calculation?
- You want to share clean data with a teammate?

With layers, you change silver logic and re-run. Without layers, you reload everything from scratch every time."

### "What if I don't know what to validate?"

**Answer:**
"Start with the basics everyone needs:
1. Primary keys unique and non-null
2. Required fields non-null
3. Data types correct

Then add business rules as you learn them. You don't have to validate everything upfront."

### "How many gold tables should I create?"

**Answer:**
"As many as you need! Each business question can be its own gold table:
- gold_daily_sales
- gold_customer_ltv
- gold_product_performance

Don't try to make one table that answers everything."

### "What if assertions fail?"

**Answer:**
"GOOD! That's the point. Now you know there's a problem. You have 3 options:
1. Fix the data (if it's a source issue)
2. Filter out bad rows (document why)
3. Adjust your assumption (maybe NULLs are OK here)

The worst thing is NOT knowing you have bad data."

---

## Potential Issues & Solutions

### Issue: Students skip validations

**Symptom:** They jump straight to analysis without assertions

**Fix:**
- Emphasize: "Validations are graded in HW3 (15 points!)"
- Show example where bad data creates wrong analysis
- Ask: "How would you explain to your boss that your revenue report was wrong?"

### Issue: Students confused by CREATE TABLE vs DataFrame

**Symptom:** Mix SQL and pandas operations randomly

**Fix:**
- Both are fine! Either:
  - SQL all the way: `CREATE TABLE silver AS ...`
  - Pandas all the way: `df.to_sql('silver', ...)`
  - Or mix: Load with pandas, save with SQL
- Key: Be consistent within a layer

### Issue: Bronze layer gets skipped

**Symptom:** Students clean data while loading

**Fix:**
- Remind: "Bronze = exact copy, no transformations"
- Show: `SELECT * FROM 'file.csv'` is bronze
- Explain: "If you mess up silver, you want original to go back to"

### Issue: Too many validations

**Symptom:** Students write 20+ assertions, analysis takes forever

**Fix:**
- Guide to "essential validations":
  - Primary key uniqueness
  - Required fields non-null
  - Reasonable ranges (no negative prices)
- Say: "3-5 good validations beat 20 shallow ones"

---

## In-Class Exercise: Grading

**Total: 5% of course grade**

**Rubric:**
- Part 1 - Bronze (1 pt): Loaded raw data correctly
- Part 2 - Silver cleaning (1 pt): Applied transformations
- Part 3 - Silver validations (1.5 pts): At least 2 meaningful assertions
- Part 4 - Gold (1 pt): Created business metric
- Part 5 - Risk note (0.5 pts): Documented an assumption or limitation

**Grading tips:**
- This is completion-based, not perfection-based
- If they attempted all parts, they likely get full credit
- Deduct only for missing sections or completely wrong approach
- Grade quickly (5-10 min per notebook)
- Common issues:
  - Missing assertions → lose Part 3 points
  - No gold table → lose Part 4 points
  - Otherwise very forgiving

**Time to grade:** ~15 minutes for 15-20 students

---

## HW3 Overview (for reference)

**Due:** Oct 29, 23:59 (1 week after Day 3)

**Scope:**
- Chicago business licenses (50K rows, CSV)
- NYC building permits (20K rows, JSON)
- Build complete bronze → silver → gold pipeline
- At least 3 validations
- 5 business KPIs
- Full documentation

**Student workload:** 6-8 hours

**Grading:** 100 points
- Correctness (40%)
- Data thinking (25%)
- Reproducibility (20%)
- Communication (15%)

**Common mistakes to watch for:**
- Not normalizing NYC JSON properly
- Missing validations
- Gold queries don't actually answer business questions
- Absolute paths instead of relative
- No documentation of assumptions

---

## Final Exam Overview (for reference)

**When:** Day 3, Block B (immediately after HW3 presentation)
**Duration:** 60 minutes
**Format:** Paper/pen, closed-book
**Points:** 100 (25% of course grade)

**Coverage:**
- SQL fundamentals (WHERE, GROUP BY, HAVING)
- Joins (INNER, LEFT, diagnosing issues)
- Window functions (ROW_NUMBER, concept)
- JSON normalization
- Data validations (assertions)
- Pipeline patterns (bronze/silver/gold)
- Data thinking (NULLs, business impact)

**What students need to know:**
- Write SQL from memory (no autocomplete!)
- Explain concepts clearly
- Debug broken queries
- Think about business implications

**Preparation:**
- Review all Day 1-3 notebooks
- Practice SQL by hand
- Understand window functions conceptually
- Know how to handle NULLs

---

## Day 3 Learning Outcomes

By end of Day 3, students should be able to:

✅ **Conceptual:**
- Explain why layered pipelines matter
- Articulate difference between bronze/silver/gold
- Understand fail-fast principle
- Recognize common data quality issues

✅ **Technical:**
- Write assertions to validate data
- Build 3-layer pipeline (bronze → silver → gold)
- Handle NULLs appropriately
- Create idempotent SQL queries

✅ **Professional:**
- Document data assumptions
- Communicate data quality issues
- Justify cleaning decisions
- Write reproducible pipelines

---

## Pacing Reminders

**Things that take longer than expected:**
- Live coding (always add 5 min buffer)
- Student questions during examples
- Technical issues (someone's DuckDB won't load)

**Things that take less time than expected:**
- Concept explanations (students get it faster than you think)
- Code walkthroughs (if you don't explain every line)

**If running behind:**
- Cut data survival tips from 15 → 10 min (focus on top 3 issues)
- Shorten bronze/silver/gold intro by 2-3 min
- Keep validations and exercise time sacred

**If running ahead:**
- Extra Q&A time
- Show alternative approaches (SQL vs pandas)
- Preview HW3 dataset structure
- Don't end early - students value full time

---

## Post-Class Actions

**Immediately after class:**
- [ ] Collect in-class exercise notebooks
- [ ] Release HW3 assignment on Moodle
- [ ] Post Day 3 teaching notebook
- [ ] Remind students: Exam is next session

**Within 24 hours:**
- [ ] Grade in-class exercises (quick, 15 min total)
- [ ] Post grades to Moodle
- [ ] Answer any follow-up questions on forum

**Before next class:**
- [ ] Print exam copies (one per student + spares)
- [ ] Prepare answer sheets
- [ ] Review exam solutions
- [ ] Bring timer for 60-minute limit

---

## Key Messages for Day 3

1. **Pipelines are quality control for data** - Just like manufacturing
2. **Fail fast saves time** - Catch problems early, not during presentation to boss
3. **Validation is not optional** - It's how you sleep at night
4. **Document your assumptions** - Future you will thank present you
5. **Reproducibility matters** - Your analysis should work on anyone's machine

---

**Have a great Day 3! You've got this.** 🚀
