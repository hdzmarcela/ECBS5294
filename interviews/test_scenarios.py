"""
Test script to verify all interview scenarios load correctly and queries work.
Run this before conducting interviews to ensure data integrity.
"""

import duckdb
import os

def test_scenario_1():
    """Test E-Commerce Analytics scenario"""
    print("=" * 70)
    print("TESTING SCENARIO 1: E-Commerce Analytics")
    print("=" * 70)

    con = duckdb.connect(':memory:')

    # Load data
    base_path = "scenario_1_ecommerce/data"
    con.execute(f"CREATE TABLE customers AS SELECT * FROM '{base_path}/customers.csv'")
    con.execute(f"CREATE TABLE orders AS SELECT * FROM '{base_path}/orders.csv'")
    con.execute(f"CREATE TABLE order_items AS SELECT * FROM '{base_path}/order_items.csv'")
    con.execute(f"CREATE TABLE products AS SELECT * FROM '{base_path}/products.csv'")

    # Verify table counts
    print("\nTable Row Counts:")
    for table in ['customers', 'orders', 'order_items', 'products']:
        count = con.execute(f"SELECT COUNT(*) as cnt FROM {table}").df()['cnt'][0]
        print(f"  {table}: {count} rows")

    # Test Q1: Orders in March 2024 > $100, delivered
    print("\n Test Q1 (Delivered orders in March > $100):")
    result = con.execute("""
        SELECT COUNT(*) as cnt
        FROM orders
        WHERE order_status = 'delivered'
          AND order_date >= '2024-03-01'
          AND order_date < '2024-04-01'
          AND total_amount > 100
    """).df()
    print(f"  Found {result['cnt'][0]} matching orders ✅")

    # Test Q2: Revenue by category
    print("\n  Test Q2 (Revenue by product category):")
    result = con.execute("""
        SELECT p.category, COUNT(DISTINCT oi.order_id) as orders, SUM(oi.price * oi.quantity) as revenue
        FROM order_items oi
        JOIN products p ON oi.product_id = p.product_id
        JOIN orders o ON oi.order_id = o.order_id
        WHERE o.order_status = 'delivered'
        GROUP BY p.category
        ORDER BY revenue DESC
        LIMIT 3
    """).df()
    print(result.to_string(index=False))

    # Test Q3: CA customers who ordered in March but not April
    print("\n  Test Q3 (CA customers: March yes, April no):")
    result = con.execute("""
        SELECT DISTINCT c.customer_id, c.customer_city
        FROM customers c
        JOIN orders o_march ON c.customer_id = o_march.customer_id
        LEFT JOIN orders o_april ON c.customer_id = o_april.customer_id
            AND o_april.order_date >= '2024-04-01'
            AND o_april.order_date < '2024-05-01'
        WHERE c.customer_state = 'CA'
          AND o_march.order_date >= '2024-03-01'
          AND o_march.order_date < '2024-04-01'
          AND o_april.order_id IS NULL
    """).df()
    print(f"  Found {len(result)} customers ✅")

    # Check NULL percentage in customer_state
    print("\n  Data Quality Check (NULL customer_state):")
    total = con.execute("SELECT COUNT(*) as cnt FROM customers").df()['cnt'][0]
    nulls = con.execute("SELECT COUNT(*) as cnt FROM customers WHERE customer_state IS NULL").df()['cnt'][0]
    pct = (nulls / total) * 100
    print(f"  {nulls}/{total} customers have NULL state ({pct:.1f}%) ✅")

    print("\n✅ Scenario 1 tests PASSED!\n")
    con.close()

def test_scenario_2():
    """Test SaaS Product Analytics scenario"""
    print("=" * 70)
    print("TESTING SCENARIO 2: SaaS Product Analytics")
    print("=" * 70)

    con = duckdb.connect(':memory:')

    # Load data
    base_path = "scenario_2_saas/data"
    con.execute(f"CREATE TABLE users AS SELECT * FROM '{base_path}/users.csv'")
    con.execute(f"CREATE TABLE subscriptions AS SELECT * FROM '{base_path}/subscriptions.csv'")
    con.execute(f"CREATE TABLE feature_usage AS SELECT * FROM '{base_path}/feature_usage.csv'")
    con.execute(f"CREATE TABLE support_tickets AS SELECT * FROM '{base_path}/support_tickets.csv'")

    # Verify table counts
    print("\nTable Row Counts:")
    for table in ['users', 'subscriptions', 'feature_usage', 'support_tickets']:
        count = con.execute(f"SELECT COUNT(*) as cnt FROM {table}").df()['cnt'][0]
        print(f"  {table}: {count} rows")

    # Test Q1: Active subscriptions
    print("\n  Test Q1 (Active subscriptions as of 2024-04-15):")
    result = con.execute("""
        SELECT COUNT(*) as active_subs
        FROM subscriptions
        WHERE end_date IS NULL OR end_date > '2024-04-15'
    """).df()
    print(f"  Active subscriptions: {result['active_subs'][0]} ✅")

    # Test Q2: MRR by plan type
    print("\n  Test Q2 (MRR by plan type):")
    result = con.execute("""
        SELECT plan_type, COUNT(*) as subs, SUM(monthly_price) as mrr
        FROM subscriptions
        WHERE end_date IS NULL OR end_date > '2024-04-15'
        GROUP BY plan_type
        ORDER BY mrr DESC
    """).df()
    print(result.to_string(index=False))

    # Test Q3: Inactive users (30+ days)
    print("\n  Test Q3 (Users inactive 30+ days):")
    result = con.execute("""
        SELECT COUNT(*) as inactive_users
        FROM users
        WHERE last_login <= '2024-03-16' OR last_login IS NULL
    """).df()
    print(f"  Inactive users (30+ days): {result['inactive_users'][0]} ✅")

    # Check NULL last_login
    print("\n  Data Quality Check (NULL last_login):")
    nulls = con.execute("SELECT COUNT(*) as cnt FROM users WHERE last_login IS NULL").df()['cnt'][0]
    print(f"  {nulls} users have NULL last_login ✅")

    print("\n✅ Scenario 2 tests PASSED!\n")
    con.close()

def test_scenario_3():
    """Test Retail Operations scenario"""
    print("=" * 70)
    print("TESTING SCENARIO 3: Retail Store Operations")
    print("=" * 70)

    con = duckdb.connect(':memory:')

    # Load data
    base_path = "scenario_3_retail/data"
    con.execute(f"CREATE TABLE stores AS SELECT * FROM '{base_path}/stores.csv'")
    con.execute(f"CREATE TABLE employees AS SELECT * FROM '{base_path}/employees.csv'")
    con.execute(f"CREATE TABLE transactions AS SELECT * FROM '{base_path}/transactions.csv'")
    con.execute(f"CREATE TABLE inventory AS SELECT * FROM '{base_path}/inventory.csv'")

    # Verify table counts
    print("\nTable Row Counts:")
    for table in ['stores', 'employees', 'transactions', 'inventory']:
        count = con.execute(f"SELECT COUNT(*) as cnt FROM {table}").df()['cnt'][0]
        print(f"  {table}: {count} rows")

    # Test Q1: CA stores with sales > $50K in April
    print("\n  Test Q1 (CA stores with April sales > $50K):")
    result = con.execute("""
        SELECT s.store_name, s.city, SUM(t.amount) as total_sales
        FROM stores s
        JOIN transactions t ON s.store_id = t.store_id
        WHERE s.state = 'CA'
          AND t.transaction_date >= '2024-04-01'
          AND t.transaction_date < '2024-05-01'
        GROUP BY s.store_name, s.city
        HAVING SUM(t.amount) > 50000
        ORDER BY total_sales DESC
    """).df()
    print(f"  Found {len(result)} qualifying stores")
    print(result.to_string(index=False) if len(result) > 0 else "  (No stores met criteria - this is okay for testing)")

    # Test Q2: Avg transaction by region
    print("\n  Test Q2 (Avg transaction amount by region):")
    result = con.execute("""
        SELECT s.region, COUNT(*) as txns, ROUND(AVG(t.amount), 2) as avg_amount
        FROM stores s
        JOIN transactions t ON s.store_id = t.store_id
        GROUP BY s.region
        ORDER BY avg_amount DESC
    """).df()
    print(result.to_string(index=False))

    # Test Q3: Out-of-stock with recent sales
    print("\n  Test Q3 (Out-of-stock products with April 8-15 sales):")
    result = con.execute("""
        SELECT DISTINCT i.product_sku, i.product_name, s.store_name
        FROM inventory i
        JOIN stores s ON i.store_id = s.store_id
        JOIN transactions t ON i.store_id = t.store_id AND i.product_sku = t.product_sku
        WHERE i.stock_level = 0
          AND t.transaction_date >= '2024-04-08'
          AND t.transaction_date <= '2024-04-15'
        ORDER BY s.store_name
        LIMIT 5
    """).df()
    print(f"  Found {len(result)} product/store combinations")
    if len(result) > 0:
        print(result.to_string(index=False))

    # Q4 check: Stores with no transactions
    print("\n  Test Q4 (Stores with no transactions - for discussion):")
    total_stores = con.execute("SELECT COUNT(*) as cnt FROM stores").df()['cnt'][0]
    stores_with_txns = con.execute("""
        SELECT COUNT(DISTINCT store_id) as cnt FROM transactions
    """).df()['cnt'][0]
    stores_without = total_stores - stores_with_txns
    print(f"  Total stores: {total_stores}")
    print(f"  Stores with transactions: {stores_with_txns}")
    print(f"  Stores WITHOUT transactions: {stores_without} ✅")
    print(f"  (These {stores_without} stores would be excluded by INNER JOIN)")

    print("\n✅ Scenario 3 tests PASSED!\n")
    con.close()

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("INTERVIEW SCENARIO DATA VALIDATION")
    print("=" * 70 + "\n")

    # Change to interviews directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    try:
        test_scenario_1()
        test_scenario_2()
        test_scenario_3()

        print("=" * 70)
        print("ALL SCENARIOS TESTED SUCCESSFULLY!")
        print("=" * 70)
        print("\nYou're ready to conduct interview simulations! 🎯\n")

    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")
        raise
