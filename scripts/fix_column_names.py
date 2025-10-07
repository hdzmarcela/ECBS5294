#!/usr/bin/env python3
"""
Fix column names in teaching notebooks to match actual cafe sales dataset.
The dataset has columns with spaces, not underscores.
"""

import json
import sys

def fix_column_names_in_sql(text):
    """Replace column names with underscores to quoted names with spaces."""
    replacements = {
        'Payment_Method': '"Payment Method"',
        'Transaction_ID': '"Transaction ID"',
        'Transaction_Date': '"Transaction Date"',
        'Date': '"Transaction Date"',  # Also fix if we used "Date" instead
        # Price is actually "Price Per Unit" in the dataset
        # We need to be careful here - only replace when it's a column reference
    }

    result = text
    for old, new in replacements.items():
        result = result.replace(old, new)

    # Special handling for Price -> "Price Per Unit"
    # Replace Price when it appears as a column name (not in strings or comments)
    # This is a bit tricky - we need to be careful not to replace "Price" in text
    import re

    # Replace Price when it's used as a column name
    # Patterns: SELECT Price, FROM Price, WHERE Price, ORDER BY Price, etc.
    result = re.sub(r'\bPrice\s*([,\s]|$|>|<|=|!|\*|/|\+|-|\)|IS)', r'"Price Per Unit"\1', result)

    # Also handle "Price AS" and similar
    result = re.sub(r'\bPrice\s+(AS|as)\s+', r'"Price Per Unit" AS ', result)

    # Handle "Price * Quantity" specifically
    result = re.sub(r'\bPrice\s*\*', r'"Price Per Unit" *', result)

    return result

def fix_notebook(notebook_path):
    """Fix all SQL code cells in a notebook."""
    print(f"Processing {notebook_path}...")

    with open(notebook_path, 'r') as f:
        nb = json.load(f)

    changes = 0
    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            # Check if cell contains SQL code
            source = ''.join(cell['source'])
            if 'con.execute' in source or 'FROM cafe' in source:
                new_source = fix_column_names_in_sql(source)
                if new_source != source:
                    # Convert back to list of lines
                    cell['source'] = new_source.split('\n')
                    # Ensure each line ends with \n except the last
                    cell['source'] = [line + '\n' for line in cell['source'][:-1]] + [cell['source'][-1]]
                    changes += 1

    if changes > 0:
        with open(notebook_path, 'w') as f:
            json.dump(nb, f, indent=1)
        print(f"  ✅ Fixed {changes} cells")
    else:
        print(f"  ℹ️  No changes needed")

    return changes

if __name__ == '__main__':
    notebooks = [
        'notebooks/day1_block_b_01_sql_foundations.ipynb',
        'notebooks/day1_block_b_02_aggregations.ipynb',
    ]

    total_changes = 0
    for nb_path in notebooks:
        try:
            changes = fix_notebook(nb_path)
            total_changes += changes
        except FileNotFoundError:
            print(f"  ⚠️  File not found: {nb_path}")
        except Exception as e:
            print(f"  ❌ Error: {e}")

    print(f"\n✅ Total cells fixed: {total_changes}")
