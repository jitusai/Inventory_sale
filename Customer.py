import mysql.connector
import db_config as dc
import pandas as pd

class Customers:
    def __init__(self):
        self.conn = dc.connect()
        self.cursor = self.conn.cursor()

    # --- Function For Adding New Customers ---
    def add_customer(self):
        name = input("Enter the Customer Name: ")
        phone = input("Enter The Phone Number(10 Digits): ")
        self.validate_customer(name, phone)
        customer_id = self.generate_customer_id()
        query = "Insert Into Customers (customer_id,name,phone) values(%s,%s,%s)"
        values = (customer_id, name, phone)
        try:
            self.cursor.execute(query, values)
            self.conn.commit()
            print(f"Customer Added Successfully and Id ={customer_id}")
        except mysql.connector.Error as err:
            print(f"Error:{err}")
        finally:
            self.cursor.close()
            self.conn.close()

    # --- For Viewing  Customers
    def view_customers(self):
        query = "Select * from Customers"
        try:
            self.cursor.execute(query)
            customers = self.cursor.fetchall()
            if len(customers) == 0:
                print("No Record Found.")
            else:
                page_size = 15
                total = len(customers)
                pages = (total + page_size - 1)//page_size
                current_page = 0
                while True:
                    start = current_page * page_size
                    end = start + page_size
                    print(f"\n---page{current_page + 1} of {pages}---")
                    for c in customers[start:end]:
                        print(f"CID:{c[0]}, Name:{c[1]}, Phone:{c[2]}")
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
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            self.cursor.close()
            self.conn.close()

    # --- Function For Deleting Existing Customers --
    def delete_customer(self):
        customer_id = input("Enter the Customer Id to Delete(CUST-001): ")
        if not self.customer_exists(customer_id):
            print(f"Error: Customer with ID {customer_id} does not Exist.")
            return
        if Customers.confirm("Are you sure you want to delete this Product? (Y/N): "):
            query = "delete from Customers where customer_id=%s"
            try:
                self.cursor.execute(query,(customer_id,))
                self.conn.commit()
                if self.cursor.rowcount == 0:
                    print("No Customer Found With That Customer_id.")
                else:
                    print("Customer is Deleted")
            except mysql.connector.Error as err:
                print(f"Error:{err}")
            finally:
                self.cursor.close()
                self.conn.close()

    # --- Export Our Customers Into CSV
    def export_to_csv(self, filename="data/customers.csv"):
        try:
            self.cursor.execute("select * from customers")
            rows = self.cursor.fetchall()
            columns = [desc[0] for desc in self.cursor.description]
            df = pd.DataFrame(rows, columns=columns)
            df.to_csv(filename, index=False)
            print("Customers Exported Successfully.")
        except Exception as e:
            print(f"Export Failed: {e}")

    # ---  Functions For Importing Customers
    def import_from_csv(self, filename="data/customers.csv"):
        try:
            df = pd.read_csv(filename)
            for _,i in df.iterrows():
                self.cursor.execute(
                    "insert into customers (customer_id, name, phone) values (%s, %s, %s)",
                    (i["customer_id"], i["name"], i["phone"]))
                self.conn.commit()
            print("Customers Imported Successfully.")
        except Exception as e:
            print(f"Import Failed: {e}")



    # --- For Auto Generating Unique Customer_id ---
    def generate_customer_id(self):
        try:
            self.cursor.execute("SELECT customer_id FROM customers ORDER BY customer_id DESC LIMIT 1")
            result = self.cursor.fetchone()
            if result and result[0]:
                last_id = int(result[0][5:])
                new_id = f"CUST-{last_id + 1:03d}"
            else:
                new_id = "CUST-001"
            return new_id
        except mysql.connector.Error as err:
            print("Error Generating Product ID:", err)
            return None

    @staticmethod
    # --- For Validating The Customer Fields ---
    def validate_customer(name, phone):
        if not name or not isinstance(name, str) or name.strip() == "":
            raise ValueError("Name must be  a Non_Empty String.")
        if not phone.isdigit() or len(phone) != 10:
            raise ValueError("Phone Number Should be 10_Digit Numeric String.")
    def customer_exists(self, customer_id):
        self.cursor.execute("select * from customers where customer_id = %s", (customer_id,))
        return self.cursor.fetchone() is not None
    @staticmethod
    def confirm(prompt="Are you sure? (Y/N): "):
        while True:
            choice = input(prompt).lower()
            if choice in ['y', 'yes']:
                return True
            elif choice in ['n', 'no']:
                return False
            else:
                print("Please enter 'y' or 'yes' or 'n' or 'no'.")



