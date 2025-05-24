import os.path

import db_config as dc
from decimal import Decimal


class Billing:

    def __init__(self):
        self.conn = dc.connect()
        self.cursor = self.conn.cursor()

    # Generating Bill By Invoice Number
    def generate_invoice(self, sale_id):
        try:
            tax_rate = 0.05
            # Fetch sale details with customer and product info
            query = '''
            SELECT s.sale_id, c.name AS customer_name, c.phone,
            p.name AS product_name, p.price, s.quantity, s.sale_date
                FROM sales s
                JOIN customers c ON s.customer_id = c.customer_id
                JOIN products p ON s.product_id = p.product_id
                WHERE s.sale_id = %s
            '''
            self.cursor.execute(query, (sale_id,))
            result = self.cursor.fetchone()

            if not result:
                print(" No sale found with that ID.")
                return

            sale_id, customer_name, phone, product_name, price, quantity, sale_date = result
            subtotal = price * quantity
            tax = subtotal * Decimal(tax_rate)
            total = subtotal + tax

            # Invoice content
            invoice_content = f'''
            ================================
                    STORE INVOICE
            ================================

            Invoice No : {sale_id}
            Date       : {sale_date}

            Customer   : {customer_name}
            Phone      : {phone}

            Product    : {product_name}
            Unit Price : {price:.2f}
            Quantity   : {quantity}
            
            --------------------------
            Subtotal   : {subtotal:.2f}
            Tax (5%)   : {tax:.2f}
            Total Bill : {total:.2f}
            ================================
            Thank you for shopping with us!
            ================================
            '''
            invoice_file = f"reports/invoices/invoice_{sale_id}.txt"
            with open(invoice_file, "w", encoding="utf-8") as file:
                file.write(invoice_content.strip())

                print(f" Invoice generated and saved to {invoice_file}")

        except Exception as e:
            print(f" Error generating invoice: {str(e)}")
        finally:
            self.cursor.close()
            self.conn.close()
    @staticmethod
    def view_invoice(invoice_no):
        invoice_file = f"reports/invoices/invoice_{invoice_no}.txt"
        if not os.path.exists(invoice_file):
            print(f"\n No Invoice No Found With That Invoice No: {invoice_no}")
            return
        print(f"Invoice for given number {invoice_no}")
        with open(invoice_file,"r") as file:
            print(file.read())
