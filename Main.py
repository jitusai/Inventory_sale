from product import Products
from Customer import Customers
from Sales import Sales
from Billing import Billing
def main():
    while True:
        print("\n*** Inventory and Sales Tracking System ***")
        print("1. Product Management")
        print("2. Customer Management")
        print("3. Sales Processing")
        print("4. Billing and Reporting")
        print("5. Exit")
        choice = input("Enter your Choice: ")
        if choice == '1':
            product_menu()
        elif choice == '2':
            customer_menu()
        elif choice == '3':
            sales_menu()
        elif choice =='4':
            billing_menu()
        elif choice == '5':
            print("Exit")
            break
        else:
            print("Invalid Choice")
def product_menu():
    while True:
        print("\n*****Product Management*****")
        print(
            "\n1.Add Product\n2.Search Product\n3.View All Products\n4.Update product\n5.delete product\n6.Export data\n7.Import data\n8.Stock Alert1 \n9.Back to main menu")
        choice = input("Enter Your Choice: ")
        try:
            if choice == '1':
                Products().add_product()
            elif choice == '2':
                Products().search_product()
            elif choice == '3':
                Products().view_all()
            elif choice == '4':
                Products().update_product()
            elif choice == '5':
                Products().delete_product()
            elif choice == '6':
                Products().export_to_csv()
            elif choice == '7':
                Products().import_from_csv()
            elif choice == '8':
                try:
                    threshold = int(input("Enter Low Stock Threshold (Default 5): ") or "5")
                except ValueError:
                    threshold = 5
                Products().stock_alerts(low_stock_threshold=threshold)
            elif choice == '9':
                break
            else:
                print("Invalid Choice Please Try again.")
        except ValueError as ve:
            print(f"Input Error: {ve}")
        except Exception as e:
            print(f"An Error Occurred: {e}")

def customer_menu():
    while True:
        print("\n*****Customer Management*****")
        print(
            "\n1.Add customer\n2.View customers\n3.delete customer\n4.Export data\n5.Import data\n6.Back to main menu")
        choice = input("Enter Your Choice:")
        try:
            if choice == '1':
                Customers().add_customer()
            elif choice == '2':
                Customers().view_customers()
            elif choice == '3':
                Customers().delete_customer()
            elif choice == '4':
                Customers().export_to_csv()
            elif choice == '5':
                Customers().import_from_csv()
            elif choice == '6':
                break
            else:
                print("Invalid choice please Try again.")
        except ValueError as ve:
            print(f"Input Error: {ve}")
        except Exception as e:
            print(f"An error occurred: {e}")


def sales_menu():
    s = Sales()

    while True:

        print("\n--- Sales Menu ---")

        print("1. Record Sale")

        print("2. View All Sales")

        print("3. Daily Summary")

        print("4. Monthly Summary")

        print("5. Yearly Summary")

        print("6. Export Sales to CSV")

        print("7. Back to Main Menu")


        choice = input("Enter choice: ")

        if choice == '1':

            try:

                cust_id = input("Customer ID(Enter CUST-000): ")

                prod_id = input("Product ID(pr000): ")

                qty = int(input("Quantity: "))

                s.record_sale(cust_id, prod_id, qty)

            except ValueError:

                print("Invalid input. IDs must be strings and Quantity must be integers.")

        elif choice == '2':

            s.view_sales()

        elif choice == '3':

            s.daily_summary()

        elif choice == '4':
            months=[1,2,3,4,5,6,7,8,9,10,11,12]
            try:

                year = int(input("Enter Year (YYYY): "))

                month = int(input("Enter Month (1-12): "))
                if len(str(year))==4 and month in months:
                    s.monthly_summary(year, month)
                else:
                    print("Enter Valid year or month")

            except ValueError:

                print("Enter valid numeric values.")

        elif choice == '5':

            try:

                year = int(input("Enter Year (YYYY): "))
                if len(str(year))==4:
                    s.yearly_summary(year)
                else:
                    print("Enter a Valid year.")

            except ValueError:

                print("Enter valid year.")

        elif choice == '6':

            s.export_sales_to_csv()

        elif choice=='7':

            break

        else:
            print("Invalid choice.")
    s.close()

def billing_menu():
    bill = Billing()
    while True:
        print("\n*****Billing and Reporting Menu*****")
        print("1.Generate Bill for a customer")
        print("2.Back to Main menu")
        choice = input("Enter your choice: ")
        if choice == '1':
            try:
                invoice_no = input("Enter your Invoice number(Ex:001) : ").strip()
                bill.view_invoice(invoice_no)
            except ValueError:
                print("Invalid customer ID. Please enter a number.")
        elif choice == '2':
            break
        else:
            print("Invalid choice. Please select again.")

if __name__ == "__main__":
    main()
