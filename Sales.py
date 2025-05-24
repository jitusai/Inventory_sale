import db_config as dc
from Billing import Billing
from datetime import date
import pandas as pd


class Sales:
    def __init__(self):
        self.conn = dc.connect()
        self.cursor = self.conn.cursor()

    # --- For Recording the Sales Into the DataBase
    def record_sale(self, customer_id,product_id,quantity):
        try:
            if not isinstance(quantity,int):
                raise ValueError("Quantity must be Integers.")
            self.cursor.execute("SELECT quantity, name FROM products WHERE product_id = %s", (product_id,))
            result = self.cursor.fetchone()

            if not result:
                print(" Product Not Found or Check The ProductId or Customer_id.")
                return
            available_qty, product_name = result

            if quantity > available_qty:
                print(f" Not Enough Stock. Available Quantity: {available_qty}")
                return
            query = "INSERT INTO sales (customer_id, product_id, quantity, sale_date) VALUES (%s, %s, %s, %s)"
            values = (customer_id, product_id, quantity, date.today())
            self.cursor.execute(query, values)
            sale_id=self.cursor.lastrowid
            new_qty = available_qty - quantity
            self.cursor.execute("UPDATE products SET quantity = %s WHERE product_id = %s", (new_qty, product_id))
            self.conn.commit()
            print(f"Sale recorded for '{product_name}'. Remaining stock: {new_qty}")
            Billing.generate_invoice(self,sale_id)

        except Exception as e:
            print(" Error recording sale:", e)
  # -- For Viewing All the Recorded Sales
    def view_sales(self):
        try:
            self.cursor.execute("""SELECT s.sale_id, c.name AS customer, p.name AS product, s.quantity, s.sale_date FROM sales s
            JOIN customers c ON s.customer_id = c.customer_id JOIN products p ON s.product_id = p.product_id
            ORDER BY s.sale_date  """)
            rows = self.cursor.fetchall()
            print("\n--- Sales Records ---")
            if len(rows) == 0:
                print("No Sales Found")
            else:
                page_size = 15
                total = len(rows)
                pages = (total + page_size - 1)//page_size
                current_page = 0
                while True:
                    start = current_page * page_size
                    end = start + page_size
                    print(f"\n---page{current_page + 1} of {pages}---")
                    for r in rows[start:end]:
                        print(f"sale_Id:{r[0]}, customer_id:{r[1]}, product_id:{r[2]}, quantity:{r[3]}, sale_date:{r[4]}")
                    print("\n N - Next | P - Previous | E - Exit")
                    choice = input("Enter Your Choice: ").strip().lower()
                    if choice == 'n' and current_page < pages - 1:
                        current_page += 1
                    elif choice == 'p' and current_page > 0:
                        current_page -= 1
                    elif choice == 'e':
                        break
                    else:
                        print("Invalid Choice or no more Pages.")
        except Exception as e:
            print(" Error viewing sales:", e)
    # --- Showing Daily Sales Summary
    def daily_summary(self):
        try:
            self.cursor.execute(""" SELECT p.name, SUM(s.quantity) AS total_sold FROM sales s
                    JOIN products p ON s.product_id = p.product_id
                    WHERE s.sale_date = CURDATE()
                    GROUP BY p.name""")
            print("\nDaily Sales Summary:")
            day_sale=self.cursor.fetchall()
            if len(day_sale)==0:
                print("No Sales are Done Today")
            else:
                for row in day_sale:
                    print(f"Product: {row[0]}, Quantity Sold: {row[1]}")
        except Exception as e:
            print("Error Fetching Daily Summary:", e)

    # ---For Shows Monthly Sales Summary
    def monthly_summary(self, year, month):
        try:
            query = """
            SELECT p.name, SUM(s.quantity)
            FROM sales s JOIN products p ON s.product_id = p.product_id
             WHERE YEAR(s.sale_date) = %s AND MONTH(s.sale_date) = %s 
             GROUP BY p.name"""
            self.cursor.execute(query, (year, month))
            print(f"\nMonthly Summary ({month}/{year}):")
            m_sale=self.cursor.fetchall()
            if len(m_sale)==0:
                print("No Monthly Sales Found ")
            else:
                for row in m_sale:
                    print(f"Product: {row[0]}, Quantity Sold: {row[1]}")
        except Exception as e:
            print("Error fetching monthly summary:", e)

    # --- For Showing the Yearly Sales Summary
    def yearly_summary(self, year):
        try:
            query = """
            SELECT p.name, SUM(s.quantity)
                    FROM sales s
                    JOIN products p ON s.product_id = p.product_id
                    WHERE YEAR(s.sale_date) = %s
                    GROUP BY p.name """
            self.cursor.execute(query, (year,))
            print(f"\nYearly Summary ({year}):")
            y_sales = self.cursor.fetchall()
            if len(y_sales)==0:
                print("No Sales Found on that Year ")
            else:
                for row in y_sales:
                    print(f"Product: {row[0]}, Quantity Sold: {row[1]}")
        except Exception as e:
            print("Error Fetching Yearly Summary:", e)

    # --- For Exporting Sales To CSV ---
    def export_sales_to_csv(self):
        try:
            self.cursor.execute("""
            SELECT s.sale_id, c.name AS customer, p.name AS product, s.quantity, s.sale_date
            FROM sales s
            JOIN customers c ON s.customer_id = c.customer_id
            JOIN products p ON s.product_id = p.product_id
            ORDER BY s.sale_date DESC
            """)
            rows = self.cursor.fetchall()
            columns = [desc[0] for desc in self.cursor.description]
            df = pd.DataFrame(rows, columns=columns)
            filename = "Data/sales.csv"
            df.to_csv(filename, index=False)
            print(f"Sales exported to {filename}")
        except Exception as e:
            print("Error exporting sales:", e)
    def close(self):
        self.cursor.close()
        self.conn.close()