import db_config as dc
import mysql.connector
import pandas as pd

class Products:
    def __init__(self):
        self.conn = dc.connect()
        self.cursor = self.conn.cursor()

    # -- For Adding New Product --
    def add_product(self):
        try:
            name = input("Enter The  Product Name: ")
            category = input("Enter The Product Category: ")
            price = float(input("Set The Price of the Product: "))
            quantity = int(input("Product Quantity: "))
            self.validate_add_product(name, category, price, quantity)
            product_id=self.generate_product_id()
            query= "Insert into Products(product_id,name,category,price,quantity) values(%s,%s,%s,%s,%s)"
            values=(product_id,name,category,price,quantity)
            self.cursor.execute(query,values)
            self.conn.commit()
            print(f"Product Added Successful with Product Id {product_id}")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            self.cursor.close()
            self.conn.close()

    # --Function for viewing all the Products --
    def view_all(self):
        query = "Select * from Products"
        try:
            self.cursor.execute(query)
            products = self.cursor.fetchall()
            if len(products)==0:
                print("No Record Found.")
            else:
                page_size = 15
                total=len(products)
                pages=(total+page_size-1)// page_size
                current_page=0
                while True:
                    start = current_page*page_size
                    end=start + page_size
                    print(f"\n---page{current_page + 1} of {pages}---")
                    for p in products[start:end]:
                        print(f"PID:{p[0]}, Name:{p[1]}, Category:{p[2]}, Price:{p[3]}, Quantity:{p[4]}")
                    print("\n N - Next | P - Previous | E - Exit")
                    choice = input("Enter Your Choice: ").strip().lower()
                    if choice =='n'  and current_page < pages -1:
                        current_page +=1
                    elif choice =='p' and current_page > 0:
                        current_page -=1
                    elif choice == 'e':
                        break
                    else:
                        print("Invalid Choice or No More Pages.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            self.cursor.close()
            self.conn.close()

    # -- Updating the Existing Products --
    def update_product(self):
        product_id = (input("Enter The Product Id To Update (Ex:pr001): ")).lower()
        if not Products().product_exists(product_id):
            print(f"Error : Product with ID {product_id} does not exist.")
            return
        field = input("Enter The Field Name To Update (Name or Category or Price or Quantity) : ").lower()
        available_fields = ['name','category','quantity','price']
        if field not in available_fields:
            print("Enter Valid Field Name ")
            return
        new_value = input("Enter The New Value: ")
        query = f"Update Products set {field} = %s Where product_id = %s"
        try:
            self.cursor.execute(query,(new_value,product_id))
            self.conn.commit()
            if self.cursor.rowcount > 0:
                print("Product Update Successful.")
            else:
                print("No Product Found Please Check The Product Number")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            self.cursor.close()
            self.conn.close()

    # -- Delete Existing Products --
    def delete_product(self):
        product_id = input("Enter the Product Id to Delete(EX:pr002): ").lower()
        if not Products().product_exists(product_id):
            print(f"Error: Product with Id {product_id} does not exist.")
            return
        if Products.conform("Are You sure you want to delete this Product? (Y/N): "):
            query= "delete from Products where product_id = %s"
            try:
                self.cursor.execute(query,(product_id,))
                self.conn.commit()
                if self.cursor.rowcount > 0:
                    print("Product Deleted Successfully")
                else:
                    print("No Product Found")
            except mysql.connector.Error as err:
                print(f"Error:{err}")
            finally:
                self.cursor.close()
                self.conn.close()

    # For Searching the Products in the table
    def search_product(self):
        try:
            search_by = input("U want to Search By Category or Product Name (Category,Name): ").lower().strip()
            if search_by == "category":
                category =input("Enter Category Name: ").strip()
                query = "select * from products where category= %s "
                self.cursor.execute(query,(category,),)
            elif search_by == "name":
                name =input("Enter The Product Name: ").strip()
                query = "select * from products where name= %s "
                self.cursor.execute(query,(name,))
            else:
                print("Invalid option .Please Choose 'Category' or 'Name' of the product.")
                return
            matched_products = self.cursor.fetchall()
            if  len(matched_products)==0:
                print("Products Not Found.")
            else:
                for p in matched_products:
                    print(f"PID:{p[0]}, Name:{p[1]}, Category:{p[2]}, Price:{p[3]}, Quantity:{p[4]}")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            self.cursor.close()
            self.conn.close()

    # -- For Exporting the products to CSV File--
    def export_to_csv(self, filename="Data/products.csv"):
        try:
            self.cursor.execute("select * from products")
            rows = self.cursor.fetchall()
            columns = [desc[0] for desc in self.cursor.description]
            df = pd.DataFrame(rows, columns=columns)
            df.to_csv(filename, index=False)
            print("Products Exported Successfully.")
        except Exception as e:
            print(f"Export Failed: {e}")
        finally:
            self.cursor.close()
            self.conn.close()

    # -- For Importing the Products from CSV File --
    def import_from_csv(self, filename="Data/products.csv"):
        try:
            df = pd.read_csv(filename)
            for _, row in df.iterrows():
                self.cursor.execute(
                    "insert into products (product_id, name, category, price, quantity) values (%s, %s, %s, %s, %s)",
                    (row["product_id"], row["name"], row["category"], float(row["price"]), int(row["quantity"])))
                self.conn.commit()
            print("Products Imported Successfully.")
        except Exception as e:
            print(f"Import Failed: {e}")
        finally:
            self.cursor.close()
            self.conn.close()

    # For Showing the  stock Alerts
    def stock_alerts(self, low_stock_threshold=5):
        try:
            self.cursor.execute("SELECT product_id, name, quantity FROM products")
            products = self.cursor.fetchall()
            out_of_stock = []
            low_stock = []
            for pid, name, qty in products:
                if qty == 0:
                    out_of_stock.append((pid, name))
                elif qty <= low_stock_threshold:
                    low_stock.append((pid, name, qty))
            if out_of_stock:
                print("\n*** Out-of-Stock Products ***")
                for pid, name in out_of_stock:
                    print(f"ID: {pid}, Name: {name} (OUT OF STOCK)")
            if low_stock:
                print("\n*** Low-Stock Products ***")
                for pid, name, qty in low_stock:
                    print(f"ID: {pid}, Name: {name}, Quantity: {qty}")
            if not out_of_stock and not low_stock:
                print("\nAll Products are Sufficiently Stocked.")
        except mysql.connector.Error as err:
            print("Error Checking Stock alerts:", err)
        finally:
            self.cursor.close()
            self.conn.close()

    # --Validations For User Input --
    @staticmethod
    def validate_add_product(name, category, price, quantity):
        if not name or not isinstance(name, str):
            raise ValueError("Product name must be a Non-empty String.")
        if not category or not isinstance(category, str):
            raise ValueError("Category must be a Non-Empty String.")
        if not isinstance(price, (float, int)) or price <= 0:
            raise ValueError("Price Must be a Positive Number.")
        if not isinstance(quantity, int) or quantity < 0:
            raise ValueError("Quantity must be a Non-negative Integer.")

    # --Function for Checking the "Products Exists" or  not
    #-- This Function is used While Doing Update or Deleting Products
    def product_exists(self,product_id):
        self.cursor.execute("Select * from Products where product_id=%s",(product_id,))
        return self.cursor.fetchone() is not None

    #--Function For Auto Generating Unique ProductID--
    def generate_product_id(self):
        try:
            self.cursor.execute("Select product_id From products Order By product_id Desc limit 1")
            result = self.cursor.fetchone()
            if result and result[0]:
                last_id = int(result[0][2:])
                new_id = f"pr{last_id + 1:03d}"
            else:
                new_id = "pr001"
            return new_id
        except mysql.connector.Error as err:
            print("Error generating product ID:", err)
            return None
    # Conformation While Deleting a Products
    @staticmethod
    def conform(prompt = "Are You Sure? (Y/N): "):
        while True:
            choice=input(prompt).lower()
            if choice in ['y','yes']:
                return True
            elif choice in['n','no',]:
                return False
            else:
                print("Please enter 'Y' or 'N'.")










