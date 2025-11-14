"""
Ingest CSV data into SQLite database.
Creates ecommerce.db in the project root with all tables and foreign key constraints.
"""

import csv
import sqlite3
from pathlib import Path

# Get the project root directory (parent of scripts folder)
SCRIPT_DIR = Path(__file__).parent.absolute()
PROJECT_ROOT = SCRIPT_DIR.parent
DATA_DIR = PROJECT_ROOT / 'data'
DB_PATH = PROJECT_ROOT / 'ecommerce.db'

print(f"Database will be created at: {DB_PATH}")
print(f"Reading CSV files from: {DATA_DIR}\n")

# Connect to SQLite database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Enable foreign key constraints
cursor.execute("PRAGMA foreign_keys = ON")
print("[OK] Foreign key constraints enabled")

# Drop tables if they exist (for clean re-run)
print("\nDropping existing tables if any...")
tables = ['payments', 'order_items', 'orders', 'products', 'customers']
for table in tables:
    cursor.execute(f"DROP TABLE IF EXISTS {table}")
print("[OK] Existing tables dropped")

# Create customers table
print("\nCreating customers table...")
cursor.execute("""
    CREATE TABLE customers (
        customer_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        gender TEXT,
        signup_date DATE,
        city TEXT,
        country TEXT
    )
""")
print("[OK] customers table created")

# Create products table
print("Creating products table...")
cursor.execute("""
    CREATE TABLE products (
        product_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT,
        price REAL NOT NULL,
        stock INTEGER NOT NULL
    )
""")
print("[OK] products table created")

# Create orders table
print("Creating orders table...")
cursor.execute("""
    CREATE TABLE orders (
        order_id INTEGER PRIMARY KEY,
        customer_id INTEGER NOT NULL,
        order_date TEXT NOT NULL,
        status TEXT,
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    )
""")
print("[OK] orders table created")

# Create order_items table
print("Creating order_items table...")
cursor.execute("""
    CREATE TABLE order_items (
        order_item_id INTEGER PRIMARY KEY,
        order_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        subtotal REAL NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders(order_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    )
""")
print("[OK] order_items table created")

# Create payments table
print("Creating payments table...")
cursor.execute("""
    CREATE TABLE payments (
        payment_id INTEGER PRIMARY KEY,
        order_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        payment_method TEXT,
        payment_status TEXT,
        FOREIGN KEY (order_id) REFERENCES orders(order_id)
    )
""")
print("[OK] payments table created")

# Insert data from CSV files
print("\n" + "="*50)
print("Inserting data from CSV files...")
print("="*50)

# Insert customers
print("\nInserting customers...")
customers_file = DATA_DIR / 'customers.csv'
with open(customers_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    cursor.executemany("""
        INSERT INTO customers (customer_id, name, email, gender, signup_date, city, country)
        VALUES (:customer_id, :name, :email, :gender, :signup_date, :city, :country)
    """, reader)
    conn.commit()
    print(f"[OK] Inserted {cursor.rowcount} customers")

# Insert products
print("Inserting products...")
products_file = DATA_DIR / 'products.csv'
with open(products_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    cursor.executemany("""
        INSERT INTO products (product_id, name, category, price, stock)
        VALUES (:product_id, :name, :category, :price, :stock)
    """, reader)
    conn.commit()
    print(f"[OK] Inserted {cursor.rowcount} products")

# Insert orders
print("Inserting orders...")
orders_file = DATA_DIR / 'orders.csv'
with open(orders_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    cursor.executemany("""
        INSERT INTO orders (order_id, customer_id, order_date, status)
        VALUES (:order_id, :customer_id, :order_date, :status)
    """, reader)
    conn.commit()
    print(f"[OK] Inserted {cursor.rowcount} orders")

# Insert order_items
print("Inserting order_items...")
order_items_file = DATA_DIR / 'order_items.csv'
with open(order_items_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    cursor.executemany("""
        INSERT INTO order_items (order_item_id, order_id, product_id, quantity, subtotal)
        VALUES (:order_item_id, :order_id, :product_id, :quantity, :subtotal)
    """, reader)
    conn.commit()
    print(f"[OK] Inserted {cursor.rowcount} order items")

# Insert payments
print("Inserting payments...")
payments_file = DATA_DIR / 'payments.csv'
with open(payments_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    cursor.executemany("""
        INSERT INTO payments (payment_id, order_id, amount, payment_method, payment_status)
        VALUES (:payment_id, :order_id, :amount, :payment_method, :payment_status)
    """, reader)
    conn.commit()
    print(f"[OK] Inserted {cursor.rowcount} payments")

# Verify data
print("\n" + "="*50)
print("Verifying data...")
print("="*50)

tables_to_check = {
    'customers': 'customers',
    'products': 'products',
    'orders': 'orders',
    'order_items': 'order_items',
    'payments': 'payments'
}

for table_name, table_display in tables_to_check.items():
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cursor.fetchone()[0]
    print(f"{table_display}: {count} rows")

# Verify foreign key constraints
print("\n" + "="*50)
print("Verifying foreign key constraints...")
print("="*50)

# Check for orphaned orders (orders without valid customers)
cursor.execute("""
    SELECT COUNT(*) FROM orders o
    LEFT JOIN customers c ON o.customer_id = c.customer_id
    WHERE c.customer_id IS NULL
""")
orphaned_orders = cursor.fetchone()[0]
print(f"Orphaned orders (invalid customer_id): {orphaned_orders}")

# Check for orphaned order_items (items without valid orders or products)
cursor.execute("""
    SELECT COUNT(*) FROM order_items oi
    LEFT JOIN orders o ON oi.order_id = o.order_id
    LEFT JOIN products p ON oi.product_id = p.product_id
    WHERE o.order_id IS NULL OR p.product_id IS NULL
""")
orphaned_items = cursor.fetchone()[0]
print(f"Orphaned order_items (invalid order_id or product_id): {orphaned_items}")

# Check for orphaned payments (payments without valid orders)
cursor.execute("""
    SELECT COUNT(*) FROM payments pay
    LEFT JOIN orders o ON pay.order_id = o.order_id
    WHERE o.order_id IS NULL
""")
orphaned_payments = cursor.fetchone()[0]
print(f"Orphaned payments (invalid order_id): {orphaned_payments}")

# Close connection
conn.close()

print("\n" + "="*50)
print("Database ingestion completed successfully!")
print("="*50)
print(f"Database location: {DB_PATH}")
print("\nYou can now query the database using SQLite tools or Python.")

