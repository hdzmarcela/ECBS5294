# Day 2, Block B: API Integration & JSON Normalization
## Teacher Primer

**Duration:** 75-80 minutes (15:20–16:45, including 10-min break)
**Audience:** MSBA students, Day 2 Block B
**Teaching Mode:** Demonstration-based (students watch, don't code along)
**Context:** Building on Day 1 (tidy data principles) and Day 2 Block A (joins)

---

## Learning Objectives

By the end of Block B, students will be able to:

1. **Fetch** data from REST APIs using Python's `requests` library
2. **Understand** JSON structure (objects, arrays, nesting)
3. **Navigate** nested JSON safely (`.get()` method)
4. **Explain** why nested JSON violates tidy data principles
5. **Normalize** one-to-many relationships into separate tables
6. **Use pandas** to flatten nested structures (`json_normalize()`, list comprehensions)
7. **Load** normalized data to DuckDB for SQL analysis
8. **Validate** data quality with assertions (PK uniqueness, FK integrity)
9. **Join** normalized tables to answer business questions

---

## Session Flow (75-80 minutes total)

### Part 1: API Basics & JSON Navigation (30-35 minutes)
**Notebook:** `day2_block_b_01_api_json_basics.ipynb`

---

#### 0:00-0:12 | REST API Fundamentals (12 min)

**Opening statement:**
> "Modern businesses run on APIs. Every app, dashboard, and analytics pipeline starts with data from somewhere else. Today you'll learn to fetch data from APIs and transform it for analysis."

**Materials:** Project notebook, run setup cells

**Show the big picture:**
- APIs are how you access external data (Stripe, Shopify, Salesforce, Google Analytics)
- REST is the most common API pattern (GET requests to URLs)
- JSON is the standard response format
- This is how real data pipelines start

**Demonstrate live API call:**
- Use DummyJSON products endpoint
- Point out URL structure: `https://dummyjson.com/products?limit=10`
- Show status code (200 = success)
- Show response size
- **Make it real:** "This is a free e-commerce API, but the patterns work for Shopify, Amazon, any product API"

**Key teaching moments:**
1. **Status codes matter** - 200 (success), 404 (not found), 429 (rate limit), 500 (server error)
2. **Timeout parameter** - Always set it! Without it, your script hangs forever
3. **Pagination metadata** - `total`, `limit`, `skip` tell you how to fetch all data
4. **Business relevance** - This metadata drives nightly batch jobs that sync entire catalogs

**Pedagogical tips:**
- Keep this section fast-paced (APIs are exciting, don't over-explain)
- Show the live API working (students love seeing real data)
- Connect to jobs they'll actually do ("This is how you pull Shopify orders")

**Common confusion:**
- "Do I need to memorize all status codes?" → No, just know 200=success, check docs for others
- "What if the API is down?" → Show backup file option in notebook

---

#### 0:12-0:25 | JSON Structure Deep Dive (13 min)

**Core concept:** JSON has objects (dicts), arrays (lists), and nesting

**Show the hierarchy:**
```json
{
  "products": [                    ← Array (list)
    {                              ← Object (dict)
      "id": 1,                     ← Simple value
      "title": "Widget",
      "dimensions": {...},         ← Nested object
      "tags": [...],               ← Nested array (strings)
      "reviews": [{...}, {...}]    ← Nested array (objects) - ONE-TO-MANY!
    }
  ]
}
```

**Run the exploration cells:**
1. Show `products_data.keys()` - top-level structure
2. Show first product structure - print field types
3. **Emphasize:** The `reviews` array is a one-to-many relationship

**Key business insights cell (IMPORTANT!):**
- Point out the business meaning of each nested structure:
  - `dimensions` (dict) → shipping cost calculations, warehouse planning
  - `tags` (list of strings) → recommendations, search, marketing
  - `reviews` (list of dicts) → **This is the relationship we'll normalize!**
- Frame it: "These nested structures reflect how businesses think about products"

**Navigate through levels:**
- Top-level: `product['title']`, `product['price']`
- Nested object: `product['dimensions']['width']`
- Array: `product['tags'][0]`
- Array of objects: Loop through `product['reviews']`

**Pedagogical tip:**
- Use the review loop example to show why you can't do SQL on nested JSON
- Ask: "How would you calculate average rating across ALL reviews with SQL?"
- Answer: "You can't! Reviews are trapped inside products. We need to extract them."

---

#### 0:25-0:35 | Safe JSON Navigation (10 min)

**Core concept:** Real APIs are messy - not all records have all fields

**Demonstrate the problem:**
- Try to access non-existent key → KeyError
- Point out: "In production, this crashes your entire pipeline at 3am"

**Show the solution: `.get()` method**
```python
# ❌ Crashes if missing
brand = product['brand']

# ✅ Safe with default
brand = product.get('brand', 'Unknown')
```

**Decision framework (IMPORTANT):**
- Required fields (id, title, price) → Use `[]` (crash is GOOD if they're missing)
- Optional fields (brand, warranty) → Use `.get()` with sensible default
- New fields (added recently) → Use `.get()` because old records won't have them
- Vendor-specific fields → Use `.get()` because only some records have them

**Show the production example:**
- Process multiple products
- Use `.get()` for optional fields
- Calculate derived values (discounted price)
- **No crashes!**

**Common student mistakes section:**
- Walk through all 5 mistakes (no timeout, no .get(), no status checks, etc.)
- These are learned from real production failures
- "Learn from my mistakes so you don't repeat them!"

**Optional: Quick check section**
- If time permits, let students think through the 3 questions
- Otherwise: "Read these later to test your understanding"

---

#### 0:35-0:40 | Break (5 minutes)

**Clear transition:**
> "Take 5 minutes. When we come back, we'll normalize this JSON into proper tables and load it to DuckDB for SQL analysis. This is where everything from Day 1 (tidy data) and this morning (joins) comes together."

---

### Part 2: JSON → DuckDB Pipeline (40-45 minutes)
**Notebook:** `day2_block_b_02_json_to_duckdb.ipynb`

---

#### 0:40-0:50 | The Normalization Problem (10 min)

**Opening statement:**
> "We can now fetch JSON from APIs. But we have a problem: nested JSON violates tidy data principles. One product has MANY reviews - that's not tidy. We need to separate them into different tables."

**Recall tidy data principles (Day 1):**
1. Each variable is a column ✓
2. Each observation is a row ✓
3. Each observational unit forms a table ← **This is the problem!**

**Show the problem:**
- One product with 3 nested reviews
- Ask: "If I want to count reviews, what do I count?"
- Point out: The observational units are mixed (products AND reviews in same structure)

**Business questions we want to answer:**
- Average rating across ALL reviews? (need to count reviews, not products)
- Which reviewers are most active? (need to count by reviewer)
- Reviews per product? (need to aggregate)
- **Can't answer these cleanly with nested JSON**

**The solution: Normalization**
- Create two tables: `products` (one row per product) and `reviews` (one row per review)
- Link with foreign key: `reviews.product_id → products.product_id`
- This is the relational model (connects back to Block A on joins!)

**Pedagogical tip:**
- Draw this on a whiteboard if available:
  ```
  BEFORE: Product {id, title, reviews: [{...}, {...}]}

  AFTER:
  Products table: {product_id, title, price, ...}
  Reviews table: {product_id, rating, comment, reviewer, ...}
                     ↑
                  Foreign key!
  ```

---

#### 0:50-1:03 | Normalize with Pandas (13 min)

**Core concept:** Extract nested data into separate DataFrames

**Step 1: Products table (5 min)**
- Show the list comprehension pattern
- Extract only product-level fields (id, title, price, category, brand, stock)
- **Don't** include reviews in products table
- Use `.get()` for optional fields (brand, stock)
- Create DataFrame: `pd.DataFrame(products_list)`
- Show result: 30 rows × 7 columns

**Validation pattern (CRITICAL):**
- "Never assume data is clean. Prove it with assertions."
- Show assertion examples:
  ```python
  assert df['product_id'].is_unique, "Duplicate IDs!"
  assert df['product_id'].notna().all(), "NULL IDs!"
  ```
- Frame it: "These assertions catch bugs early - much better than finding bad data in your dashboard 3 weeks later"
- Run validation on products table

**Step 2: Reviews table (8 min)**
- This is the tricky part: exploding one-to-many
- Show nested loop pattern:
  ```python
  for product in products_data['products']:
      product_id = product['id']
      for review in product.get('reviews', []):
          # Create row with product_id as FK
  ```
- **Emphasize:** We're creating a new row for EACH review
- Include `product_id` as foreign key in every review row
- Create DataFrame: `pd.DataFrame(reviews_list)`
- Show result: ~90 rows × 6 columns

**The magic moment:**
- "We started with 30 products. Now we have 90 review rows."
- "This is normalization - we've separated the data by observational unit"
- **Show the math:** 30 products × ~3 reviews each = ~90 review rows

**Foreign key integrity validation (IMPORTANT):**
- Check that every `reviews.product_id` exists in `products.product_id`
- Show what "orphaned reviews" means (reviews pointing to non-existent products)
- Business impact: Orphaned FKs break JOINs and corrupt analysis
- Run FK integrity assertion

**Pedagogical tip:**
- The nested loop pattern is the heart of normalization
- Walk through it slowly: "For each product, for each review IN that product..."
- Point out we're building a flat list from nested structure

---

#### 1:03-1:15 | Load to DuckDB & SQL Analysis (12 min)

**Why DuckDB? (2 min)**
- Fast (columnar storage, optimized for analytics)
- SQL interface (familiar syntax)
- No server (embedded, no setup)
- Works seamlessly with pandas
- "Think of it as SQLite for analytics"

**Load tables (3 min):**
```python
con.execute("CREATE TABLE products AS SELECT * FROM products_df")
con.execute("CREATE TABLE reviews AS SELECT * FROM reviews_df")
```
- Verify with `SHOW TABLES` and preview queries
- Point out: DataFrame → SQL table in one line!

**SQL Analysis (7 min):**

**Query 1: Products by category**
- GROUP BY to aggregate products
- COUNT(*) for product count, AVG(price) for average price
- Show business insights: "Groceries dominate at 50% of catalog, furniture is premium"

**Query 2: JOIN products + reviews (CRITICAL)**
- This is where it all comes together!
- LEFT JOIN to keep all products (even those without reviews)
- GROUP BY to aggregate reviews per product
- COUNT(r.rating) for review count, AVG(r.rating) for average rating
- **Teaching moment:** "This is why we normalized! Now we can JOIN and aggregate across tables"

**Connect to Block A:**
- "This morning you learned INNER/LEFT JOIN with Brazilian e-commerce data"
- "Now you're doing the same thing, but with data YOU created by normalizing JSON"
- "This is the full cycle: API → Normalize → Load → JOIN → Insights"

**Common JOIN mistakes section:**
- Walk through the 4 mistakes (missing ON clause, INNER vs LEFT, missing GROUP BY columns, COUNT(*) vs COUNT(column))
- These are based on real student errors
- Show the decision guide: "Do you need ALL left rows? → LEFT JOIN"

**Optional: Pause and Try section**
- If time permits: "Try writing the reviewer analysis query"
- Otherwise: "This is in your exercise - you'll practice it there"

---

#### 1:15-1:20 | Summary & HW2 Setup (5 min)

**What we accomplished:**
- ✅ Fetched JSON from API
- ✅ Normalized nested structures (products + reviews)
- ✅ Loaded to DuckDB
- ✅ Used SQL JOINs to answer business questions
- ✅ Validated data quality with assertions

**Key patterns they learned:**
- Normalization (separate observational units)
- Foreign keys (connect related tables)
- Pandas transformation (list comprehensions, DataFrame creation)
- DuckDB integration (SQL on pandas DataFrames)
- LEFT JOIN (keep all left rows)

**This is Homework 2!**
- Same pattern, different dataset
- Fetch from API or parse JSON file
- Normalize 2-3 related tables
- Load to DuckDB
- Write 3-5 SQL queries for business KPIs
- Add validation assertions
- Document with data dictionary

**Preview HW2 quickly:**
- 194 products with 582 reviews (full DummyJSON dataset)
- More complex nesting (tags to explode, dimensions to flatten)
- Real business scenario (TechMart acquiring QuickBuy)
- Due: Day 3, start of class
- "You now have the complete template - this notebook IS your solution pattern"

---

## Key Concepts to Emphasize

### REST APIs
- Most common way to access external data
- GET requests to URLs return JSON
- Always set timeout and check status codes
- Pagination metadata (total, limit, skip) enables full data sync

### JSON Structure
- Objects (dicts), arrays (lists), primitives
- Nesting creates complexity
- One-to-many relationships appear as nested arrays

### Safe Navigation
- Use `.get()` for optional fields
- Required fields can use `[]` (crash is good if they're missing)
- Real APIs are messy - handle missing data gracefully

### Normalization
- Nested JSON violates tidy data principle #3 (one observational unit per table)
- Extract nested arrays into separate tables
- Use foreign keys to preserve relationships
- Enables SQL JOIN and aggregation

### Data Validation
- Never assume data is clean
- Use assertions to prove data quality
- Check PK uniqueness, FK integrity, value ranges
- Fail fast with clear error messages

### DuckDB Integration
- Embedded analytical database
- SQL interface on pandas DataFrames
- One-line table creation
- Perfect for notebooks and pipelines

---

## Common Student Confusions

### "Why can't we just query JSON with SQL?"
**Address:** Some databases support JSON queries (PostgreSQL, MySQL 5.7+), but:
- Limited functionality compared to proper tables
- Slower performance
- Can't leverage indexes efficiently
- Normalization follows relational best practices

**Better answer:** "You CAN, but normalized tables give you full SQL power (JOINs, efficient aggregations, proper indexes)"

### "Why use `.get()` instead of try/except?"
**Address:** `.get()` is more concise and Pythonic for dictionary access:
```python
# ❌ Verbose
try:
    brand = product['brand']
except KeyError:
    brand = 'Unknown'

# ✅ Clean
brand = product.get('brand', 'Unknown')
```

**Teaching moment:** "There are cases for try/except (like network errors), but `.get()` is standard for dictionary access"

### "When do I use INNER vs LEFT JOIN?"
**Address:** Use the decision question: "Do I need ALL rows from the left table?"
- YES → LEFT JOIN (example: all products, even those without reviews)
- NO → INNER JOIN (example: only products that have been reviewed)

**Teaching moment:** "In analytics, LEFT JOIN is more common because you usually want to see everything, including gaps in data"

### "How do I know if my normalization is correct?"
**Address:** Check for violations of tidy data principles:
- ✅ Each variable is a column
- ✅ Each observation is a row
- ✅ Each observational unit forms a table ← Does each table represent ONE concept?

**Rule of thumb:** If you have a list of dicts in your JSON, that's probably a separate table

### "Why validate with assertions instead of just checking results?"
**Address:** Assertions serve multiple purposes:
1. **Documentation** - They state assumptions explicitly
2. **Early detection** - Catch bad data before it corrupts downstream analysis
3. **Fail fast** - Stop processing immediately with clear error message

**Teaching moment:** "In production, bad data that passes silently is worse than a crash"

---

## Pedagogical Tips

### Live API Demo (Block B Notebook 1)
- **Do:** Show the API call working in real-time (students find this exciting)
- **Do:** Point out the response size, status code, metadata
- **Don't:** Dwell on HTTP protocol details (this isn't a web development course)
- **Connect:** "This is exactly how Shopify's API works, just with authentication"

### Show Errors and Fix Them
- **Do:** Deliberately cause a KeyError, show the crash, then show `.get()` fixing it
- **Why:** Students remember fixes for problems they've seen
- **Bonus:** "I've made this mistake at 3am when my pipeline crashed - learn from me!"

### Connect to Day 1 Tidy Data
- **Callback:** "Remember Day 1 when we talked about tidy data principles?"
- **Show:** How nested JSON violates principle #3
- **Frame:** "Today we're CREATING tidy data from messy JSON - same principles, reverse direction"

### Emphasize the Complete Pipeline
- **Visual:** Draw or show: `API → JSON → Normalize → DuckDB → SQL → Insights`
- **Frame:** "This is the modern data pipeline. You're learning each step."
- **Business value:** "Companies pay six figures for data engineers who can build these pipelines"

### Use Business Language
- Frame everything with business value:
  - Not: "We're exploding arrays"
  - Instead: "We're extracting customer reviews so we can analyze satisfaction metrics"
- Connect to jobs they'll do:
  - "This is how you'd sync Stripe payment data into your warehouse"
  - "This is how marketing dashboards get data from Facebook/Google APIs"

### Normalize Timing
- API basics moves fast (APIs are intuitive)
- Normalization moves slower (this is the hard part)
- Save time for the JOIN queries at the end (the payoff!)

---

## Materials Checklist

### Before Class
- [ ] Both notebooks run end-to-end without errors
- [ ] DummyJSON API is accessible (test it!)
- [ ] Backup JSON files are in place (in case API is down)
- [ ] Quick reference printed/available: `references/json_normalization_quick_reference.md`
- [ ] HW2 README reviewed and ready to present

### During Class
- [ ] Project both notebooks clearly
- [ ] Internet connection stable (for live API demo)
- [ ] Can switch to backup files if API fails
- [ ] HW2 assignment file ready to show

### After Class
- [ ] Post both notebooks to LMS
- [ ] Post quick reference card
- [ ] Post HW2 assignment with README
- [ ] Release encrypted solution for Block A exercise

---

## HW2 Setup Guidance

**When presenting HW2:**

1. **Show the business scenario** - TechMart acquiring QuickBuy, need to integrate JSON catalog
2. **Show the dataset** - 194 products, 582 reviews, realistic complexity
3. **Connect to today's work** - "Same pattern as Notebook 2, larger scale"
4. **Emphasize deliverables:**
   - 2-3 normalized tables
   - 3-5 SQL KPIs
   - Validation assertions
   - Data dictionary
5. **Point to resources:**
   - Today's notebooks are the template
   - Quick reference has all the patterns
   - HW2 README has detailed rubric
6. **Due date:** Day 3, start of class (firm deadline)

**Common HW2 questions to preempt:**
- Q: "Can I use a different API?" → A: Yes, but DummyJSON is recommended (documented, reliable)
- Q: "How many tables?" → A: At minimum products + reviews (like today), bonus for tags or other entities
- Q: "What if I get stuck?" → A: Refer to Notebook 2 - it has the complete pattern
- Q: "How long should this take?" → A: 3-4 hours if you follow today's pattern

---

## Additional Notes

### Block B vs Block A
- **Block A:** Given clean multi-table data, learn to JOIN
- **Block B:** Given messy nested JSON, CREATE clean multi-table data, THEN JOIN
- **Synthesis:** Both blocks teach relational thinking, different entry points

### Why DuckDB and Not Just Pandas?
- **Pandas:** Good for transformation, limited for complex queries
- **DuckDB:** Full SQL power (window functions, complex JOINs, CTEs)
- **Real world:** Most companies use SQL for analytics (Snowflake, BigQuery, Redshift)
- **Teaching:** Students need SQL skills for job market

### Time Management
- If running long: Skip "Pause and Try" sections (students can do these as practice)
- If running short: Spend more time on common mistakes sections (high value)
- Always leave 5 minutes for HW2 setup

### Student Energy Management
- Block B comes after lunch and Block A (students are tired)
- The break at 35 minutes is CRITICAL - enforce it
- Keep energy high with live demos and business stories
- The payoff (SQL queries at the end) re-engages them

---

## Success Metrics

**Students are ready for HW2 if they can:**
- [ ] Fetch data from an API with proper timeout and error checking
- [ ] Navigate nested JSON structures safely using `.get()`
- [ ] Identify one-to-many relationships in JSON
- [ ] Extract nested arrays into separate DataFrames
- [ ] Create foreign key relationships between tables
- [ ] Load DataFrames to DuckDB
- [ ] Write LEFT JOIN queries with aggregation
- [ ] Add assertions to validate data quality

**If students struggle with:**
- **API basics** → Not critical (most APIs work the same, syntax is google-able)
- **Normalization logic** → CRITICAL (this is the core skill - slow down and reteach)
- **SQL JOINs** → Review Block A material (they need this from this morning)

---

## Closing Thoughts

**Day 2 Block B completes the picture:**
- Day 1 Block A: Tidy data principles ✓
- Day 1 Block B: SQL fundamentals ✓
- Day 2 Block A: SQL JOINs ✓
- **Day 2 Block B: Creating tidy data from APIs** ✓

**Students now have a complete toolkit:**
- Fetch data from external sources (APIs)
- Transform messy data into clean structure (normalization)
- Store in queryable format (DuckDB)
- Analyze with powerful SQL (JOINs, aggregations)

**This is a professional data pipeline.** Students who master this material can:
- Build ETL pipelines for businesses
- Integrate third-party data (Shopify, Stripe, Salesforce, etc.)
- Create data warehouses from API sources
- Support BI teams with clean, queryable data

**Frame the ending:**
> "You just built a complete data pipeline from scratch. Companies pay $100K+ for data engineers who can do this. You're now one of them - you just need practice. That's what HW2 is for."

---

**Contact:** Eduardo Ariño de la Rubia (RubiaE@ceu.edu)
**Last updated:** 2025-10-13
