# Tidy Data - Hadley Wickham

**Source:** https://vita.had.co.nz/papers/tidy-data.pdf
**Original Publication:** Journal of Statistical Software, 2014

## Tidy Data Definition

A tidy dataset is structured where:
- Each variable forms a column
- Each observation forms a row
- Each type of observational unit forms a table

## Five Common Problems Making Datasets Messy

1. **Column headers are values, not variable names**
   - Example: Years or categories as column names instead of a single "year" variable

2. **Multiple variables are stored in one column**
   - Example: "male_2020" combining gender and year in one column name

3. **Variables are stored in both rows and columns**
   - Example: A matrix-style layout where both rows and columns represent variables

4. **Multiple types of observational units are stored in the same table**
   - Example: Mixing customer data with transaction data in one table

5. **A single observational unit is stored in multiple tables**
   - Example: Sales data split across multiple files by month

## Key Principles

- Consistent variable naming
- Consistent data structure
- Each variable in its own column
- Each observation in its own row

## Teaching Note

From R4DS Chapter: "Tidy datasets are all alike, but every messy dataset is messy in its own way." - Hadley Wickham

Benefits:
- Consistent data structure makes it easier to learn and use tools
- Easier to work with vectorized operations
- More natural data transformations
