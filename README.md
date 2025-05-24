## Inventory and Sales Tracking System

A simple Python-based Inventory and Sales Tracking System using MySQL for backend storage. This project allows shop owners or businesses to manage products, customers, sales, and billing with CSV import/export support and invoice generation.

## Features

- Product Management: Add, update, delete, view, and search products. Stock alerts for low/out-of-stock products.
- Customer Management: Add, view, and delete customers. Import/export customer data.
- Sales Processing: Record sales, automatically update stock, and view sales history with summaries (daily, monthly, yearly).
- Billing: Generate and view invoices for each sale, with automatic calculation of tax and totals.
- Data Import/Export: Import and export data to and from CSV files for products, customers, and sales.
- Reports: Store invoice reports as text files for easy retrieval and printing.

## Folder Structure

```
inventory_sales/
├── db_config.py            # Database connection setup
├── product.py              # Product management logic
├── customer.py             # Customer management logic
├── sales.py                # Sales processing and summary logic
├── billing.py              # Invoice generation and viewing
├── main.py                 # Main menu and app logic
├── data/
│   ├── products.csv        # Product data (import/export)
│   ├── customers.csv       # Customer data (import/export)
│   └── sales.csv           # Sales data (import/export)
├── reports/
│   └── invoices/           # Folder for invoice .txt files
├── schema.sql              # MySQL schema to set up required tables
├── README.md               # This file
```

## Requirements

- Python 3.x
- MySQL Server
- [mysql-connector-python](https://pypi.org/project/mysql-connector-python/)
- Basic knowledge of running Python scripts

## Setup Instructions



1. **Install Python dependencies:**
   ```bash
   pip install mysql-connector-python
   ```

2. **MySQL Setup:**
   - Create a database named `inventory_db`.
   - Run `schema.sql` in your MySQL server to create required tables:
     ```bash
     mysql -u root -p inventory_db < schema.sql
     ```

3. **Configure Database Connection:**
   - Edit `db_config.py` with your MySQL credentials.
     ```python
     # db_config.py
     import mysql.connector
     def connect():
         return mysql.connector.connect(
             host="localhost",
             user="root",
             password="your_password",
             database="inventory_db"
         )
     ```

4. **Prepare Data Folders:**
   - Ensure the following directories exist:
     - `data/`
     - `reports/invoices/`
   - You can create them if missing:
     ```bash
     mkdir -p data reports/invoices
     ```

5. **Run the Application:**
   ```bash
   python main.py
   ```

## Usage

You will be presented with a menu-driven CLI:
- Navigate between Product Management, Customer Management, Sales Processing, and Billing/Reports.
- Operations are interactive and validated.
- Exported CSVs and generated invoices are stored in their respective folders.

## SQL Schema Example (`schema.sql`)

```sql
CREATE TABLE products (
    product_id VARCHAR(10) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    quantity INT NOT NULL
);

CREATE TABLE customers (
    customer_id VARCHAR(10) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(10) NOT NULL
);

CREATE TABLE sales (
    sale_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id VARCHAR(10),
    product_id VARCHAR(10),
    quantity INT NOT NULL,
    sale_date DATE NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
```

## Notes

- All invoice files are created in `reports/invoices/` as `.txt`.
- Input validation is enforced to prevent inconsistent data.
- Error messages are displayed for database or validation issues.
- Suitable for small businesses, academic projects, or as a starter for larger inventory systems.


