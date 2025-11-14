"""
Generate synthetic e-commerce datasets as CSV files.
All files are saved to the /data folder.
"""

import csv
import random
from datetime import datetime, timedelta
from faker import Faker
from pathlib import Path

# Get the project root directory (parent of scripts folder)
SCRIPT_DIR = Path(__file__).parent.absolute()
PROJECT_ROOT = SCRIPT_DIR.parent
DATA_DIR = PROJECT_ROOT / 'data'

# Ensure data directory exists
DATA_DIR.mkdir(exist_ok=True)

# Initialize Faker
fake = Faker()

# Configuration
NUM_CUSTOMERS = 1200
NUM_PRODUCTS = 800
NUM_ORDERS = 1500
MIN_ORDER_ITEMS = 1
MAX_ORDER_ITEMS = 5
PAYMENT_METHODS = ['Credit Card', 'Debit Card', 'PayPal', 'Bank Transfer', 'Cash on Delivery']
ORDER_STATUSES = ['Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled']
PAYMENT_STATUSES = ['Pending', 'Completed', 'Failed', 'Refunded']
PRODUCT_CATEGORIES = [
    'Electronics', 'Clothing', 'Home & Garden', 'Books', 'Sports & Outdoors',
    'Toys & Games', 'Health & Beauty', 'Automotive', 'Food & Beverages', 'Pet Supplies'
]

# Generate customers.csv
print("Generating customers.csv...")
customers = []
for i in range(1, NUM_CUSTOMERS + 1):
    customers.append({
        'customer_id': i,
        'name': fake.name(),
        'email': fake.email(),
        'gender': random.choice(['Male', 'Female', 'Other']),
        'signup_date': fake.date_between(start_date='-2y', end_date='today').strftime('%Y-%m-%d'),
        'city': fake.city(),
        'country': fake.country()
    })

with open(DATA_DIR / 'customers.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['customer_id', 'name', 'email', 'gender', 'signup_date', 'city', 'country'])
    writer.writeheader()
    writer.writerows(customers)

print(f"[OK] Generated {NUM_CUSTOMERS} customers")

# Generate products.csv
print("Generating products.csv...")
products = []
for i in range(1, NUM_PRODUCTS + 1):
    products.append({
        'product_id': i,
        'name': fake.catch_phrase() + ' ' + random.choice(['Pro', 'Premium', 'Deluxe', 'Standard', 'Basic']),
        'category': random.choice(PRODUCT_CATEGORIES),
        'price': round(random.uniform(9.99, 999.99), 2),
        'stock': random.randint(0, 500)
    })

with open(DATA_DIR / 'products.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['product_id', 'name', 'category', 'price', 'stock'])
    writer.writeheader()
    writer.writerows(products)

print(f"[OK] Generated {NUM_PRODUCTS} products")

# Generate orders.csv
print("Generating orders.csv...")
orders = []
customer_ids = list(range(1, NUM_CUSTOMERS + 1))
start_date = datetime(2023, 1, 1)
end_date = datetime.now()

for i in range(1, NUM_ORDERS + 1):
    order_date = fake.date_time_between(start_date=start_date, end_date=end_date)
    orders.append({
        'order_id': i,
        'customer_id': random.choice(customer_ids),
        'order_date': order_date.strftime('%Y-%m-%d %H:%M:%S'),
        'status': random.choice(ORDER_STATUSES)
    })

with open(DATA_DIR / 'orders.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['order_id', 'customer_id', 'order_date', 'status'])
    writer.writeheader()
    writer.writerows(orders)

print(f"[OK] Generated {NUM_ORDERS} orders")

# Generate order_items.csv
print("Generating order_items.csv...")
order_items = []
order_item_id = 1
product_ids = list(range(1, NUM_PRODUCTS + 1))
product_prices = {p['product_id']: p['price'] for p in products}

for order in orders:
    num_items = random.randint(MIN_ORDER_ITEMS, MAX_ORDER_ITEMS)
    selected_products = random.sample(product_ids, min(num_items, len(product_ids)))
    
    for product_id in selected_products:
        quantity = random.randint(1, 5)
        price = product_prices[product_id]
        subtotal = round(price * quantity, 2)
        
        order_items.append({
            'order_item_id': order_item_id,
            'order_id': order['order_id'],
            'product_id': product_id,
            'quantity': quantity,
            'subtotal': subtotal
        })
        order_item_id += 1

with open(DATA_DIR / 'order_items.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['order_item_id', 'order_id', 'product_id', 'quantity', 'subtotal'])
    writer.writeheader()
    writer.writerows(order_items)

print(f"[OK] Generated {len(order_items)} order items")

# Generate payments.csv
print("Generating payments.csv...")
payments = []
order_ids = list(range(1, NUM_ORDERS + 1))

# Calculate order totals from order_items
order_totals = {}
for item in order_items:
    order_id = item['order_id']
    if order_id not in order_totals:
        order_totals[order_id] = 0
    order_totals[order_id] += item['subtotal']

# Some orders might have multiple payment attempts (failed then succeeded)
for order_id in order_ids:
    # Most orders have one payment, some have multiple attempts
    num_payments = 1 if random.random() > 0.1 else random.randint(2, 3)
    
    order_total = order_totals.get(order_id, round(random.uniform(10.00, 1000.00), 2))
    
    for attempt in range(num_payments):
        # If multiple attempts, first ones might be failed
        if num_payments > 1 and attempt < num_payments - 1:
            payment_status = 'Failed'
            amount = order_total  # Still record the full amount
        else:
            payment_status = random.choice(['Completed', 'Completed', 'Completed', 'Pending', 'Refunded'])
            amount = order_total
        
        payments.append({
            'payment_id': len(payments) + 1,
            'order_id': order_id,
            'amount': round(amount, 2),
            'payment_method': random.choice(PAYMENT_METHODS),
            'payment_status': payment_status
        })

with open(DATA_DIR / 'payments.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['payment_id', 'order_id', 'amount', 'payment_method', 'payment_status'])
    writer.writeheader()
    writer.writerows(payments)

print(f"[OK] Generated {len(payments)} payments")

print("\n" + "="*50)
print("All datasets generated successfully!")
print("="*50)
print(f"Customers: {NUM_CUSTOMERS} rows")
print(f"Products: {NUM_PRODUCTS} rows")
print(f"Orders: {NUM_ORDERS} rows")
print(f"Order Items: {len(order_items)} rows")
print(f"Payments: {len(payments)} rows")
print(f"\nAll files saved to: {DATA_DIR}")

