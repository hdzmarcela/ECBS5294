#!/usr/bin/env python3
"""
Prepare Day 3 datasets:
1. Create Olist subsets for teaching and exercise
2. Download Chicago Business Licenses
3. Download NYC DOB Permit Issuance

This script downloads real government data from official open data portals.
"""

import pandas as pd
import json
import requests
from pathlib import Path

# Base paths
DATA_DIR = Path("data")
DAY3_DIR = DATA_DIR / "day3"
TEACHING_DIR = DAY3_DIR / "teaching"
EXERCISE_DIR = DAY3_DIR / "exercise"
HW3_DIR = DAY3_DIR / "hw3_data_pack"

# Ensure directories exist
for dir_path in [TEACHING_DIR, EXERCISE_DIR, HW3_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

print("=" * 70)
print("Day 3 Dataset Preparation")
print("=" * 70)

# =============================================================================
# Part 1: Create Olist Subsets for Teaching (Block A) and Exercise
# =============================================================================

print("\n[1/3] Creating Olist subsets for teaching and exercise...")

# Load Olist orders
olist_orders = pd.read_csv("data/day2/block_a/olist_orders_dataset.csv")
olist_customers = pd.read_csv("data/day2/block_a/olist_customers_dataset.csv")
olist_order_items = pd.read_csv("data/day2/block_a/olist_order_items_dataset.csv")

print(f"   Loaded Olist data: {len(olist_orders)} orders, {len(olist_customers)} customers")

# Create teaching subset (~1000 orders)
teaching_orders = olist_orders.sample(n=1000, random_state=42).copy()
teaching_customer_ids = teaching_orders['customer_id'].unique()
teaching_customers = olist_customers[olist_customers['customer_id'].isin(teaching_customer_ids)].copy()
teaching_order_ids = teaching_orders['order_id'].unique()
teaching_items = olist_order_items[olist_order_items['order_id'].isin(teaching_order_ids)].copy()

# Save teaching subset
teaching_orders.to_csv(TEACHING_DIR / "olist_orders_subset.csv", index=False)
teaching_customers.to_csv(TEACHING_DIR / "olist_customers_subset.csv", index=False)
teaching_items.to_csv(TEACHING_DIR / "olist_order_items_subset.csv", index=False)

print(f"   ✓ Created teaching subset: {len(teaching_orders)} orders")

# Create exercise subset (~500 orders)
exercise_orders = olist_orders.sample(n=500, random_state=123).copy()
exercise_customer_ids = exercise_orders['customer_id'].unique()
exercise_customers = olist_customers[olist_customers['customer_id'].isin(exercise_customer_ids)].copy()
exercise_order_ids = exercise_orders['order_id'].unique()
exercise_items = olist_order_items[olist_order_items['order_id'].isin(exercise_order_ids)].copy()

# Save exercise subset
exercise_orders.to_csv(EXERCISE_DIR / "mini_orders.csv", index=False)
exercise_customers.to_csv(EXERCISE_DIR / "mini_customers.csv", index=False)
exercise_items.to_csv(EXERCISE_DIR / "mini_order_items.csv", index=False)

print(f"   ✓ Created exercise subset: {len(exercise_orders)} orders")

# =============================================================================
# Part 2: Download Chicago Business Licenses (CSV)
# =============================================================================

print("\n[2/3] Downloading Chicago Business Licenses...")

# Chicago Data Portal API endpoint (using Socrata API)
# https://data.cityofchicago.org/Community-Economic-Development/Business-Licenses/r5kz-chrr
chicago_url = "https://data.cityofchicago.org/resource/r5kz-chrr.csv"

try:
    # Download with limit (we'll get ~50K rows as subset)
    print(f"   Fetching from: {chicago_url}")
    print(f"   (This may take 30-60 seconds...)")

    # Note: Socrata API returns max 1000 rows by default, we need to use $limit parameter
    chicago_df = pd.read_csv(f"{chicago_url}?$limit=50000")

    print(f"   Downloaded {len(chicago_df)} records")
    print(f"   Columns: {list(chicago_df.columns)}")

    # Save to HW3 data pack
    chicago_df.to_csv(HW3_DIR / "chicago_business_licenses.csv", index=False)
    print(f"   ✓ Saved to {HW3_DIR / 'chicago_business_licenses.csv'}")

except Exception as e:
    print(f"   ✗ Error downloading Chicago data: {e}")
    print(f"   Please download manually from: https://data.cityofchicago.org/resource/r5kz-chrr.csv")

# =============================================================================
# Part 3: Download NYC DOB Permit Issuance (JSON)
# =============================================================================

print("\n[3/3] Downloading NYC DOB Permit Issuance...")

# NYC Open Data API endpoint (using Socrata API)
# https://data.cityofnewyork.us/Housing-Development/DOB-Permit-Issuance/ipu4-2q9a
nyc_url = "https://data.cityofnewyork.us/resource/ipu4-2q9a.json"

try:
    print(f"   Fetching from: {nyc_url}")
    print(f"   (This may take 30-60 seconds...)")

    # Download JSON (limit to 20000 records)
    response = requests.get(f"{nyc_url}?$limit=20000")
    response.raise_for_status()

    nyc_data = response.json()
    print(f"   Downloaded {len(nyc_data)} records")

    # Show sample structure
    if nyc_data:
        print(f"   Sample keys: {list(nyc_data[0].keys())[:10]}...")

    # Save as JSON
    with open(HW3_DIR / "nyc_building_permits.json", 'w') as f:
        json.dump(nyc_data, f, indent=2)

    print(f"   ✓ Saved to {HW3_DIR / 'nyc_building_permits.json'}")

except Exception as e:
    print(f"   ✗ Error downloading NYC data: {e}")
    print(f"   Please download manually from: https://data.cityofnewyork.us/resource/ipu4-2q9a.json")

# =============================================================================
# Summary
# =============================================================================

print("\n" + "=" * 70)
print("Dataset Preparation Complete!")
print("=" * 70)
print("\nCreated files:")
print(f"  Teaching (Block A):")
print(f"    - {TEACHING_DIR / 'olist_orders_subset.csv'}")
print(f"    - {TEACHING_DIR / 'olist_customers_subset.csv'}")
print(f"    - {TEACHING_DIR / 'olist_order_items_subset.csv'}")
print(f"  Exercise:")
print(f"    - {EXERCISE_DIR / 'mini_orders.csv'}")
print(f"    - {EXERCISE_DIR / 'mini_customers.csv'}")
print(f"    - {EXERCISE_DIR / 'mini_order_items.csv'}")
print(f"  HW3 Data Pack:")
print(f"    - {HW3_DIR / 'chicago_business_licenses.csv'}")
print(f"    - {HW3_DIR / 'nyc_building_permits.json'}")
print("\nNext steps:")
print("  1. Review downloaded data for quality")
print("  2. Create data pack README with attribution")
print("  3. Test loading in DuckDB")
