# Day 1 Datasets

This directory contains two datasets used in Day 1 teaching materials.

---

## Dataset 1: Cafe Sales Data (Dirty)

**Source:** Kaggle - Cafe Sales Dirty Data for Cleaning Training
**URL:** https://www.kaggle.com/datasets/ahmedmohamed2003/cafe-sales-dirty-data-for-cleaning-training
**License:** CC-BY-SA-4.0
**File:** `dirty_cafe_sales.csv`
**Used in:** Day 1 Block A (Tidy Data Foundations)

---

## Dataset Description

This dataset contains 10,000 cafe sales transactions from 2023. It has been intentionally made "dirty" to practice data cleaning and tidy data principles. This is **real-world practice data** - the messiness you see here happens in production systems!

---

## Dataset Structure

### Columns

| Column Name | Expected Type | Description |
|------------|--------------|-------------|
| `Transaction ID` | string | Unique identifier for each transaction (format: TXN_XXXXXXX) |
| `Item` | string | Product purchased (Coffee, Sandwich, Cake, etc.) |
| `Quantity` | integer | Number of items purchased |
| `Price Per Unit` | float | Price per single item in dollars |
| `Total Spent` | float | Total transaction amount (should equal Quantity × Price Per Unit) |
| `Payment Method` | string | How customer paid (Cash, Credit Card, Digital Wallet) |
| `Location` | string | Transaction location (In-store, Takeaway) |
| `Transaction Date` | date | Date of transaction (format: YYYY-MM-DD) |

---

## Intentional Data Quality Issues

This dataset contains the following problems you'll need to identify and handle:

### 1. Missing Values (Multiple Representations)
- **NaN/NULL**: True missing values (pandas reads these as NaN)
- **Empty strings**: Some cells are empty but not NULL
- **Columns affected**: All columns have some missing values
- **Counts**:
  - Item: 333 NaN
  - Quantity: 138 NaN
  - Price Per Unit: 179 NaN
  - Total Spent: 173 NaN
  - Payment Method: 2,579 NaN (25%!)
  - Location: 3,265 NaN (33%!)
  - Transaction Date: 159 NaN

### 2. Sentinel Values
- **"ERROR"**: Indicates data collection or processing errors
  - Appears in: Item (~292), Total Spent (~164), Transaction Date (~142), Location
- **"UNKNOWN"**: Indicates unknown/unrecorded values
  - Appears in: Payment Method (~293), Location (~338)

### 3. Type Issues
- **All columns read as 'object' (string) type**
- Should be:
  - Quantity → integer
  - Price Per Unit → float
  - Total Spent → float
  - Transaction Date → datetime

### 4. Potential Data Integrity Issues
- **Total Spent** should equal Quantity × Price Per Unit
  - Some rows have "ERROR" instead of calculated values
  - Need to validate or recalculate
- **Transaction ID** should be unique (primary key)
  - Verify no duplicates exist

---

## What "Clean" Looks Like

After cleaning, your dataset should:

1. **Have proper types**
   - Numeric columns as int/float
   - Dates as datetime
   - Categorical columns as string (or category type)

2. **Handle missing values consistently**
   - Document your approach: Did you drop rows? Fill with defaults?
   - Be consistent (don't treat NaN differently than "UNKNOWN")

3. **Have a validated primary key**
   - Transaction ID should be unique and non-null
   - Add assertions to prove this

4. **Handle sentinel values**
   - Decide: Are "ERROR" and "UNKNOWN" missing values?
   - Convert to NaN or leave as-is? Document your choice!

5. **Validate data integrity**
   - Does Total Spent = Quantity × Price Per Unit?
   - Are there any impossible values (negative prices, zero quantity)?

---

## Exercise Questions to Answer

After cleaning the data, create a summary table that shows:

1. **Total sales by payment method**
   - How much revenue from each payment type?
   - How many transactions?

2. **Most popular items**
   - What sells the most (by quantity)?
   - What generates the most revenue?

3. **Location comparison**
   - In-store vs Takeaway: which is more popular?
   - Average transaction value by location?

---

## Learning Objectives

By working with this dataset, you'll practice:

- **Tidy data principles**: Is this dataset tidy? Why or why not?
- **Primary keys**: Identifying and validating unique identifiers
- **Type handling**: Converting strings to numbers and dates
- **Missing value strategy**: Distinguishing NULL, empty, ERROR, UNKNOWN
- **Data validation**: Using assertions to check data quality
- **Documentation**: Explaining your assumptions and choices

---

## Tips for Students

### Don't Panic!
Real-world data is messy. This is normal. Your job is to:
1. **Explore** - understand what you have
2. **Decide** - make defensible choices about how to handle issues
3. **Document** - explain what you did and why
4. **Validate** - prove your data is now clean

### Use Assertions
After cleaning, add checks like:
```python
# Primary key is unique
assert df['Transaction ID'].is_unique

# No nulls in required fields
assert df['Transaction ID'].notna().all()

# Types are correct
assert df['Quantity'].dtype in ['int64', 'Int64']
assert df['Price Per Unit'].dtype == 'float64'

# Data integrity
# (Note: this might fail if you kept ERROR rows - that's okay if documented!)
calculated_total = df['Quantity'] * df['Price Per Unit']
# Check on rows where we have all the data
mask = df['Total Spent'].notna() & (df['Total Spent'] != 'ERROR')
# ... etc
```

### Document Your Choices
For every decision, add a markdown cell explaining:
- What problem did you encounter?
- What choice did you make?
- Why did you make that choice?
- What are the implications?

Example:
> "**Handling UNKNOWN payment methods:** I found 293 transactions with payment method = 'UNKNOWN'. I chose to convert these to NaN because they represent missing data, not a separate payment type. This means our 'total sales by payment method' analysis will only include known payment methods. Alternative: Could create an 'Unknown' category, but that might mislead stakeholders into thinking this is a valid payment option."

---

## Advanced Considerations

If you finish early, explore:

1. **Date patterns**: Are there more sales on certain days/months?
2. **Anomaly detection**: Any transactions that look suspicious? (very high quantities, unusual prices)
3. **Correlation**: Does payment method correlate with location or item type?
4. **Data quality scoring**: What percentage of data is clean/usable?

---

## Need Help?

Common issues:

- **Can't load data**: Make sure you're using relative paths from repo root
- **Type conversion fails**: Handle non-numeric values (ERROR, UNKNOWN) first
- **Assertion fails**: That's good! It means you found a problem. Document it.
- **Don't know what to do**: That's normal. Make a choice, document it, move forward. You can always revise.

Remember: There's rarely one "correct" answer in data cleaning. What matters is making **defensible, documented choices**.

---
---

## Dataset 2: Sample - Superstore

**Source:** Kaggle - Sample Supermarket Dataset
**URL:** https://www.kaggle.com/datasets/bravehart101/sample-supermarket-dataset
**License:** CC0 (Public Domain)
**File:** `Sample - Superstore.csv`
**Used in:** Day 1 Block B (SQL with DuckDB - Window Functions)

---

## Dataset Description

This is a classic retail dataset containing ~10,000 orders from a fictional U.S. superstore over a 4-year period (2015-2018). It includes detailed information about products, customers, sales, and profits across multiple categories and regions.

This dataset is **clean and well-structured** - perfect for learning SQL aggregations and window functions without the distraction of data quality issues.

---

## Dataset Structure

### Columns

| Column Name | Type | Description |
|------------|------|-------------|
| `Row ID` | integer | Unique row identifier |
| `Order ID` | string | Unique order identifier (multiple rows can share an Order ID) |
| `Order Date` | date | Date when order was placed (MM/DD/YYYY) |
| `Ship Date` | date | Date when order was shipped |
| `Ship Mode` | string | Shipping method (Second Class, Standard Class, etc.) |
| `Customer ID` | string | Unique customer identifier |
| `Customer Name` | string | Customer's full name |
| `Segment` | string | Customer segment (Consumer, Corporate, Home Office) |
| `Country` | string | Country (United States) |
| `City` | string | Customer's city |
| `State` | string | Customer's state |
| `Postal Code` | integer | Customer's postal/ZIP code |
| `Region` | string | Geographic region (South, West, East, Central) |
| `Product ID` | string | Unique product identifier |
| `Category` | string | Product category (Furniture, Office Supplies, Technology) |
| `Sub-Category` | string | Product sub-category (Bookcases, Chairs, Labels, etc.) |
| `Product Name` | string | Full product name |
| `Sales` | float | Sales amount in dollars |
| `Quantity` | integer | Number of items ordered |
| `Discount` | float | Discount percentage (0-1) |
| `Profit` | float | Profit amount in dollars (can be negative) |

---

## Dataset Characteristics

### Size
- **Rows:** 9,994 orders
- **Columns:** 21
- **Time period:** 2015-2018 (4 years)
- **Customers:** ~800 unique customers
- **Products:** Multiple categories and sub-categories

### Data Quality
- ✅ Clean data (no missing values)
- ✅ Consistent types
- ✅ Valid date ranges
- ✅ Realistic business data
- ✅ No duplicates in Row ID
- ⚠️ Order ID is NOT unique (multiple products per order)

### Why This Dataset?

**Perfect for SQL teaching because:**
1. **Time series data:** 4 years of daily transactions (great for window functions)
2. **Multiple orders per customer:** Ideal for ROW_NUMBER() and "latest per group" patterns
3. **Hierarchical categories:** Good for GROUP BY practice
4. **Clean data:** Focus on SQL syntax, not data cleaning
5. **Realistic business context:** Students understand retail scenarios

---

## Key Learning Applications

### Block B: SQL with DuckDB

**Notebook 1: SQL Foundations**
- Basic SELECT, WHERE, ORDER BY
- Filtering by date ranges, categories, regions
- Calculated columns (profit margin, discount impact)

**Notebook 2: Aggregations**
- GROUP BY: Sales by category, region, customer
- HAVING: Filtering aggregated results
- Multiple aggregation functions

**Notebook 3: Window Functions**
- **ROW_NUMBER():** Latest order per customer, top 3 products per category
- **LAG():** Month-over-month sales comparisons
- **Moving averages:** 7-day moving average of daily sales
- Mental model: Windows preserve rows vs GROUP BY collapses

---

## Common Analysis Patterns

Students will use this dataset to answer questions like:

1. **Customer behavior:**
   - Who are our top customers by total sales?
   - What's the most recent order for each customer?
   - How many repeat customers do we have?

2. **Product performance:**
   - Which categories generate the most profit?
   - What are the top 5 products by sales in each category?
   - Which products have negative profit (unprofitable)?

3. **Time series:**
   - What's the month-over-month sales growth?
   - Are there seasonal patterns in sales?
   - What's the 7-day moving average of daily sales?

4. **Regional analysis:**
   - Which regions are most profitable?
   - Do different regions prefer different product categories?
   - Average order value by region?

---

## Data Integrity Notes

### Primary Keys
- **Row ID:** Unique row identifier (primary key for rows)
- **Order ID:** NOT unique - same order can contain multiple products
- **Customer ID + Order Date:** Customers can place multiple orders on the same day

### Relationships
- One customer → Many orders
- One order → Many products (rows)
- One product → Many orders

### Validation Checks

```python
# Check uniqueness
assert superstore['Row ID'].is_unique  # ✅ Should pass
assert not superstore['Order ID'].is_unique  # ✅ Correct - multiple products per order

# Check date validity
assert superstore['Order Date'].min() >= pd.Timestamp('2015-01-01')
assert superstore['Ship Date'] >= superstore['Order Date']  # Ships after order

# Check data ranges
assert superstore['Discount'].between(0, 1).all()  # Discounts are 0-100%
assert superstore['Quantity'] > 0  # Can't order 0 items
```

---

## License & Attribution

**License:** CC0 (Public Domain)

This dataset is released under the Creative Commons Zero (CC0) license, which places it in the public domain. This means:
- ✅ Free to use for any purpose (including commercial)
- ✅ No attribution required (but appreciated!)
- ✅ Can be modified and redistributed
- ✅ No restrictions

**Original Source:** This is a variant of the classic Tableau Superstore sample dataset, made available on Kaggle under CC0 license.

**Attribution:** While not required, proper attribution is good academic practice:
> Sample Superstore Dataset. (2020). Retrieved from https://www.kaggle.com/datasets/bravehart101/sample-supermarket-dataset. Licensed under CC0 (Public Domain).

---

## Comparison: Cafe Sales vs Superstore

| Aspect | Cafe Sales | Superstore |
|--------|-----------|-----------|
| **Purpose** | Data cleaning practice | SQL query practice |
| **Data Quality** | Intentionally messy | Clean and structured |
| **Size** | 10,000 rows | 10,000 rows |
| **Time Span** | 2023 (1 year) | 2015-2018 (4 years) |
| **Primary Key** | Transaction ID | Row ID |
| **Teaching Focus** | Tidy data, validation | SQL, aggregations, windows |
| **Block** | Block A | Block B |
| **Difficulty** | Beginner | Intermediate |

---

## Need Help?

**Common issues:**

- **Encoding errors:** Use `encoding='latin-1'` when reading the CSV
  ```python
  df = pd.read_csv('data/day1/Sample - Superstore.csv', encoding='latin-1')
  ```

- **Date parsing:** Dates are in MM/DD/YYYY format
  ```python
  df['Order Date'] = pd.to_datetime(df['Order Date'])
  ```

- **Relative paths:** Always use paths relative to repo root
  ```python
  # ✅ Correct
  'data/day1/Sample - Superstore.csv'

  # ❌ Wrong
  '/Users/yourname/project/data/...'
  ```

---

**For more information about either dataset, see the Day 1 teaching notebooks in `notebooks/day1_block_*.ipynb`**
