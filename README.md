# Omnicommerce Data Pipeline

A complete e-commerce data pipeline project that generates synthetic data, ingests it into SQLite, and provides analytics queries.

## Project Structure

```
omnicommerce-data-pipeline/
├── data/                    # CSV data files
│   ├── customers.csv
│   ├── products.csv
│   ├── orders.csv
│   ├── order_items.csv
│   └── payments.csv
├── scripts/
│   ├── generate_data.py    # Generate synthetic e-commerce data
│   ├── ingest_to_sqlite.py # Ingest CSV data into SQLite
│   ├── test_queries.py     # Execute SQL queries with formatted output
│   └── verify_project.py   # Verify project completeness
├── sql/                     # SQL analytics queries
│   ├── monthly_revenue.sql
│   ├── best_sellers.sql
│   ├── top_customers.sql
│   ├── order_full_details.sql
│   └── complete_order_analysis.sql
├── ecommerce.db            # SQLite database (generated)
└── README.md
```

## Features

### 1. Synthetic Data Generation
- Generates 5 realistic CSV datasets using Faker
- Maintains referential integrity across all tables
- 1000+ rows per dataset

### 2. Database Ingestion
- Creates SQLite database with proper schema
- Implements foreign key constraints
- Validates data integrity

### 3. Analytics Queries
- Monthly revenue reports
- Best selling products analysis
- Top customers by order frequency
- Complete order details with all joins

### 4. Query Execution
- Automated query execution script
- Beautiful formatted output using Rich library
- Supports all SQL files in `/sql` folder

## Setup

### Prerequisites
- Python 3.7+
- pip

### Installation

1. Clone the repository:
```bash
git clone https://github.com/SpMonish84/omnicommerce-data-pipeline.git
cd omnicommerce-data-pipeline
```

2. Install dependencies:
```bash
pip install faker rich
```

## Usage

### Step 1: Generate Synthetic Data
```bash
python scripts/generate_data.py
```
This creates 5 CSV files in the `/data` folder.

### Step 2: Ingest Data into SQLite
```bash
python scripts/ingest_to_sqlite.py
```
This creates `ecommerce.db` and populates all tables.

### Step 3: Run Analytics Queries
```bash
python scripts/test_queries.py
```
This executes all SQL queries and displays formatted results.

### Verify Project Completeness
```bash
python scripts/verify_project.py
```

## Database Schema

- **customers**: customer_id (PK), name, email, gender, signup_date, city, country
- **products**: product_id (PK), name, category, price, stock
- **orders**: order_id (PK), customer_id (FK), order_date, status
- **order_items**: order_item_id (PK), order_id (FK), product_id (FK), quantity, subtotal
- **payments**: payment_id (PK), order_id (FK), amount, payment_method, payment_status

## SQL Queries

All queries are located in the `/sql` folder:
- `monthly_revenue.sql` - Revenue analysis by month
- `best_sellers.sql` - Top selling products
- `top_customers.sql` - Most active customers
- `order_full_details.sql` - Complete order information
- `complete_order_analysis.sql` - Comprehensive analysis joining all tables

