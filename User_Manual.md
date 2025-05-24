# Inventory and Sales Tracking System - User Manual

Welcome to the Inventory and Sales Tracking System! This guide will walk you through every menu and submenu, explaining what each part does and how to use it efficiently.

---

## Table of Contents

- [Starting the Program](#starting-the-program)
- [Main Menu Overview](#main-menu-overview)
- [Product Management (Submenu Details)](#product-management-submenu-details)
- [Customer Management (Submenu Details)](#customer-management-submenu-details)
- [Sales Processing (Submenu Details)](#sales-processing-submenu-details)
- [Billing and Reporting (Submenu Details)](#billing-and-reporting-submenu-details)
- [Exiting the System](#exiting-the-system)
- [Common Errors & Tips](#common-errors--tips)
- [FAQs](#faqs)

---

## Starting the Program

1. Ensure all required files (`product.py`, `Customer.py`, `Sales.py`, `Billing.py`) are in the same directory.
2. Open your terminal and run:
   ```
   python main.py
   ```
3. The main menu will appear.

---

## Main Menu Overview

On launch, you’ll see:

```
*** Inventory and Sales Tracking System ***
1. Product Management
2. Customer Management
3. Sales Processing
4. Billing and Reporting
5. Exit
```

Type the number of your choice and press Enter.

---

## Product Management (Submenu Details)

Choose **1** from the main menu.

### Product Management Menu Options

1. **Add Product**
   - You’ll be prompted to enter product details such as name, product ID, price, and stock quantity.
   - The system adds this product to your records.

2. **View Products**
   - Displays a list/table of all products with details like ID, name, price, and stock.

3. **Update Product**
   - Enter the product’s ID you want to update.
   - The system will prompt you for new values for each field (name, price, quantity, etc.).
   - Leave a field blank if you do not want to change it.

4. **Delete Product**
   - Enter the product’s ID to permanently remove it from the system.
   - The system will ask for confirmation before deleting.

5. **Export Data**
   - Saves the current product list to a CSV file.
   - You’ll be asked for a filename or use the default.
   - Use this for backup or to open data in Excel.

6. **Import Data**
   - Load products from a CSV file.
   - You’ll be prompted for the CSV filename.
   - Imported products will be added to your current list.

7. **Search Product**
   - Enter keywords (name, ID, etc.) to look for specific products.
   - Results matching your query will be shown.

8. **Stock Alert**
   - Enter a threshold (e.g., 5) to see which products are below this stock level.
   - Default threshold is 5 if you just press Enter.

9. **Back to Main Menu**
   - Return to the main menu.

---

## Customer Management (Submenu Details)

Choose **2** from the main menu.

### Customer Management Menu Options

1. **Add Customer**
   - Enter details like customer name, unique customer ID, and contact info.
   - The customer is added to your records.

2. **View Customers**
   - Lists all customers with their IDs, names, and contact information.

3. **Delete Customer**
   - Enter the customer’s ID to remove them from the system.
   - The system will ask for confirmation.

4. **Export Data**
   - Export all customer data to a CSV file for backup or use in other apps.

5. **Import Data**
   - Import customer data from a CSV file.

6. **Back to Main Menu**
   - Return to the main menu.

---

## Sales Processing (Submenu Details)

Choose **3** from the main menu.

### Sales Menu Options

1. **Record Sale**
   - You’ll be prompted for:
     - **Customer ID:** Enter as `CUST-000` (or as your format).
     - **Product ID:** Enter as e.g., `pr000`.
     - **Quantity:** How many units were sold.
   - The sale is logged and inventory is updated.

2. **View All Sales**
   - Shows a list of all sales transactions, including date, product, customer, and quantity.

3. **Daily Summary**
   - Displays today’s total sales, including the number of transactions and total revenue.

4. **Monthly Summary**
   - Prompts for a year and a month.
   - Shows all sales and totals for that month.

5. **Yearly Summary**
   - Prompts for a year.
   - Shows sales summary for the entire year.

6. **Export Sales to CSV**
   - Save sales data to a CSV file for records or further analysis.

7. **Import Sales From CSV**
   - Load sales data from a CSV file. Useful for restoring previous sales logs.

8. **Back to Main Menu**
   - Return to the main menu.

---

## Billing and Reporting (Submenu Details)

Choose **4** from the main menu.

### Billing and Reporting Menu Options

1. **Generate Bill for a Customer**
   - Enter the **Invoice Number** (Sale ID).
   - The system retrieves and displays the invoice/bill for that sale, including items, quantities, prices, and total amount.

2. **Back to Main Menu**
   - Return to the main menu.

---

## Exiting the System

- Choose **5** from the main menu.
- The system will display "Exit" and close.

---

## Common Errors & Tips

- **Invalid Menu Choices:** If you type an invalid number, you’ll see “Invalid choice please try again.”
- **Input Errors:** If you enter incorrect data (e.g., text instead of numbers), you’ll be prompted to enter valid data.
- **ID Formats:** Use the formats suggested (e.g., `CUST-000` for customers, `pr000` for products).
- **CSV Files:** Always check your CSV format before importing. Back up existing data before importing new files.
- **Leave Fields Blank:** When updating, you can leave fields blank to keep them unchanged.
- **Stock Alerts:** Use the stock alert feature to avoid running out of products.

---

## FAQs

**Q1: What happens if I try to add a product with an existing ID?**  
A: The system will notify you and not allow duplicate product IDs.

**Q2: Can I undo a delete operation?**  
A: No. Deleting a product or customer is permanent. Always double-check before confirming a delete.

**Q3: How do I view invoices later?**  
A: All invoices are saved as text files in the `reports/invoices/` directory for future reference.

**Q4: What format should my CSV files be in for import?**  
A: The CSV files should match the exported format from the system. Column headers and order must be preserved.

**Q5: What if I enter the wrong value by mistake?**  
A: The system will show an error and let you try again.

**Q6: Can I use this system on multiple computers?**  
A: Yes, as long as all dependencies and the database are set up correctly and you use the same data files/database.

---