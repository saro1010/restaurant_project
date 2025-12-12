import psycopg2 
from psycopg2 import sql 
from psycopg2 import errors

class Database:
    def connect(self):
        return psycopg2.connect(
            dbname="restaurant_db",
            user="postgres",
            password="YOUR_PASSWORD",
            host="localhost",
            port="5432"
        )


class MenuManager:
    def __init__(self, db):
        self.db = db

    def add_item(self):
        name = input("Enter the name of item : ")
        price = float(input("Enter price: "))
        price = round(price, 2)

        conn = self.db.connect()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO menu_items(name, price) VALUES (%s, %s)",
            (name, price)
        )

        conn.commit()
        cur.close()
        conn.close()

        print("item added successfully")

    def show_menu(self):
        conn = self.db.connect()
        cur = conn.cursor()

        cur.execute("SELECT item_id, name, price FROM menu_items ORDER BY item_id")
        rows = cur.fetchall()

        if not rows:
            print("menu is empty!")
            cur.close()
            conn.close()
            return

        for item_id, name, price in rows:
            print(f"{item_id}. {name} - ${price:.2f}")

        cur.close()
        conn.close()
    
    def update_item(self):
        self.show_menu()
        print()

        try:
            item_id = int(input("Enter item ID to update : "))
        except ValueError:
            print("Please enter a valid number.")
            return

        new_name = input("Enter new name for item : ")
        new_price = float(input("Enter new price for item : "))
        new_price = round(new_price, 2)

        conn = self.db.connect()
        cur = conn.cursor()

        cur.execute(
            "UPDATE menu_items SET name = %s, price = %s WHERE item_id = %s",
            (new_name, new_price, item_id)
        )

        conn.commit()

        if cur.rowcount == 0:
            print("No item found with that ID.")
        else:
            print("Item updated successfully.")

        cur.close()
        conn.close()


    def delete_item(self):
        self.show_menu()
        print()

        try:
            item_id = int(input("Enter item ID to delete : "))
        except ValueError:
            print("Please enter a valid number.")
            return 

        conn = self.db.connect()
        cur = conn.cursor()

        cur.execute("DELETE FROM menu_items WHERE id = %s", (item_id,))
        conn.commit()

        if cur.rowcount == 0:
            print("No item found with that ID.")
        else:
            print("Item deleted successfully.")

        cur.close()   
        conn.close()


class TableManager:

    def __init__(self, db):
        self.db = db

    def add_table(self):
        try:
            table_number = int(input("Please enter the table number: "))
        except ValueError:
            print("Please enter a valid number.")
            return

        conn = self.db.connect()
        cur = conn.cursor()

        try:
            cur.execute("INSERT INTO tables (table_number) VALUES (%s)", (table_number,))
            conn.commit()
            print("Table added successfully.")

        except psycopg2.errors.UniqueViolation:
            
            print("This table number already exists!")
            conn.rollback()

        finally:
            cur.close()
            conn.close()


    def view_tables(self):

        conn = self.db.connect()
        cur = conn.cursor()
        cur.execute("SELECT * FROM tables ORDER BY table_number")
        rows = cur.fetchall()
        
        if not rows:
            print("No table found!")
        else:            
            for table_id, table_number, status in rows:
                print(f"Table {table_number} (ID: {table_id}) - Status: {status}")

        cur.close()
        conn.close()

    def update_table_status(self):
        self.view_tables()
        print()

        try:
            table_id = int(input("Select the table ID to update: "))
        except ValueError:
            print("Please enter a valid number.")
            return

        new_status = input("Enter the new status (available, reserved, occupied): ").lower()

        valid_status = ["available", "reserved", "occupied"]

        if new_status not in valid_status:
            print("Invalid status!")
            return

        conn = self.db.connect()
        cur = conn.cursor()

        cur.execute(
            "UPDATE tables SET status = %s WHERE id = %s",
            (new_status, table_id))

        conn.commit()

        if cur.rowcount == 0:
            print("No table found with that ID.")
        else:
            print("Table status updated successfully.")

        cur.close()
        conn.close()

    def delete_table(self):
        self.view_tables()
        print()

        try:
            table_id = int(input("Select the table ID to delete: "))
        except ValueError:
            print("Please enter a valid number.")
            return      

        conn = self.db.connect()
        cur = conn.cursor() 
        cur.execute('DELETE FROM tables WHERE id = %s', (table_id,))
        conn.commit()

        if cur.rowcount == 0:
            print("No table found with that ID.")
        else:
            print("Table deleted successfully.")

        cur.close()
        conn.close()

class OrderManager:
    def __init__(self, db):
        self.db = db

    def create_order(self):
        pass

    def add_item_to_order(self):
        pass

    def view_order_details(self):
        pass

    def view_active_orders(self):
        pass

    def calculate_daily_sales(self):
        pass


class RestaurantApp:
    def __init__(self):
        self.db = Database()
        self.menu_manager = MenuManager(self.db)
        self.table_manager = TableManager(self.db)
        self.order_manager = OrderManager(self.db)

    def main_menu(self):
        while True:
            print("\n----- Restaurant Manager -----")
            print("1. Menu Management")
            print("2. Table Management")
            print("3. Order Management")
            print("4. Exit")
            choice = input("Choose an option: ")

            pass

    def menu_management_menu(self):
        pass

    def table_management_menu(self):
        pass

    def order_management_menu(self):
        pass


if __name__ == "__main__":
    app = RestaurantApp()
    app.main_menu()
