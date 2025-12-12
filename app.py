import psycopg2 
from psycopg2 import sql 
from psycopg2 import errors

class Database:
    def connect(self):
        return psycopg2.connect(
            dbname="restaurant_db",
            user="postgres",
            password="saRO7577",
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

        cur.execute('SELECT status FROM tables WHERE id = %s', (table_id,))
        row = cur.fetchone()

        if row is None:
            print("No table found with that ID.")
            cur.close()
            conn.close()
            return

        status = row[0]

        if status == "occupied":
            print("Table status is occupied! You can't delete occupied tables.")
            cur.close()
            conn.close()
            return

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

        print("\n---- available tables ----\n")
        conn = self.db.connect()
        cur = conn.cursor() 

        cur.execute("SELECT id FROM tables WHERE status = %s", ('available',))
        rows = cur.fetchall()
        if not rows:
            print("No available tables!")
            cur.close()
            conn.close()
            return

        for (t_id,) in rows:
            print(f"Table ID: {t_id}")

        try:
            table_id = int(input("Enter table ID for order: "))
        except ValueError:
            print("Please enter a valid number.")
            cur.close()
            conn.close()
            return

        available_ids = [t[0] for t in rows]

        if table_id not in available_ids:
            print("Table is occupied or does not exist!")
            cur.close()
            conn.close()
            return
        
        cur.execute(
        "INSERT INTO orders (table_id, status) VALUES (%s, %s) RETURNING id",
        (table_id, "open"))

        order_id = cur.fetchone()[0]

        cur.execute("UPDATE tables SET status = %s WHERE id = %s", ("occupied", table_id))
        conn.commit()

        print(f"Order created successfully! Order ID: {order_id}")

        cur.close()
        conn.close()


    def add_item_to_order(self):

        try:
            item_id = int(input("Enter the item id please : "))
            order_id = int(input("Enter the order id please : "))
            quantity = int(input("Enter quantity please : "))
        except ValueError:
            print("Please enter a valid number.")
            return
        
        if quantity <= 0:
            print("Quantity must be greater than 0.")
            return

        conn = self.db.connect()
        cur = conn.cursor()

        cur.execute("SELECT 1 FROM menu_items WHERE id = %s", (item_id,))

        if cur.fetchone() is None:
            print(f"item id {item_id} does not exist!")
            cur.close()
            conn.close()
            return
        
        cur.execute("SELECT status FROM orders WHERE id = %s", (order_id,))
        order_status_row = cur.fetchone()

        if order_status_row is None:
            print(f"order id {order_id} does not exist!")
            cur.close()
            conn.close()
            return

        status = order_status_row[0]

        if status != "open":
            print("This order is not open. You can't add items to it.")
            cur.close()
            conn.close()
            return

        cur.execute(
            "INSERT INTO order_details(order_id, item_id, quantity) VALUES (%s, %s, %s)",
            (order_id, item_id, quantity)
        )

        conn.commit()
        print("item added to order successfully.")

        cur.close()
        conn.close()


    def view_order_details(self):
        try:
            order_id = int(input("Enter order ID: "))
        except ValueError:
            print("Please enter a valid number.")
            return

        conn = self.db.connect()
        cur = conn.cursor()

        cur.execute("SELECT status, table_id, order_time FROM orders WHERE id = %s", (order_id,))
        order_row = cur.fetchone()

        if order_row is None:
            print("Order not found.")
            cur.close()
            conn.close()
            return
        
        cur.execute("""
        SELECT mi.name, mi.price, od.quantity, (mi.price * od.quantity) AS line_total
        FROM order_details od
        JOIN menu_items mi ON mi.id = od.item_id
        WHERE od.order_id = %s """, (order_id,))
        rows = cur.fetchall()

        if not rows:
            print("This order has no items.")
            cur.close()
            conn.close()
            return

        status, table_id, order_time = order_row
        print(f"Order {order_id} | Table ID: {table_id} | Status: {status} | Time: {order_time}")


        total = 0
        print("\n--- Order Details ---")
        for name, price, quantity, line_total in rows:
            price = float(price)
            line_total = float(line_total)
            print(f"{name} | ${price:.2f} | qty: {quantity} | line total: ${line_total:.2f}")
            total += line_total

        print(f"\nTotal: ${total:.2f}")

        cur.close()
        conn.close()

    def view_active_orders(self):
        
        conn = self.db.connect()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT o.id, t.table_number, o.order_time, o.status
            FROM orders o
            JOIN tables t ON t.id = o.table_id
            WHERE o.status = %s
            ORDER BY o.order_time DESC
        """, ("open",))

        rows = cur.fetchall()

        if not rows:
            print("No active orders.")
            cur.close()
            conn.close()
            return

        print("\n--- Active Orders ---")
        for order_id, table_number, order_time, status in rows:
            print(f"Order {order_id} | Table {table_number} | {order_time} | Status: {status}")

        cur.close()
        conn.close()

    def close_order(self):
        try:
            order_id = int(input("Enter order ID: "))
        except ValueError:
            print("Please enter a valid number.")
            return

        conn = self.db.connect()
        cur = conn.cursor()

        cur.execute("SELECT status, table_id FROM orders WHERE id = %s", (order_id,))
        row = cur.fetchone()

        if row is None:
            print("Order not found.")
            cur.close()
            conn.close()
            return

        status, table_id = row

        if status != "open":
            print("Order is not open.")
            cur.close()
            conn.close()
            return

        cur.execute("UPDATE orders SET status = %s WHERE id = %s", ("closed", order_id))
        cur.execute("UPDATE tables SET status = %s WHERE id = %s", ("available", table_id))

        conn.commit()
        print("Order closed successfully and table is now available.")

        cur.close()
        conn.close()
       

    def calculate_daily_sales(self):
        conn = self.db.connect()
        cur = conn.cursor()

        cur.execute("""
            SELECT COALESCE(SUM(mi.price * od.quantity), 0)
            FROM orders o
            JOIN order_details od ON od.order_id = o.id
            JOIN menu_items mi ON mi.id = od.item_id
            WHERE o.status = %s
            AND o.order_time::date = CURRENT_DATE
        """, ('closed',))
            
        row = cur.fetchone()
        total = float(row[0])
            
        print(f"Total sales today: ${total:.2f}")

        cur.close()
        conn.close()


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
