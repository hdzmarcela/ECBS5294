# Day 1 Exercise Dataset: Cafe Sales Data

**Source:** Kaggle - Cafe Sales Dirty Data for Cleaning Training
**URL:** https://www.kaggle.com/datasets/ahmedmohamed2003/cafe-sales-dirty-data-for-cleaning-training
**License:** CC-BY-SA-4.0
**File:** `dirty_cafe_sales.csv`

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
