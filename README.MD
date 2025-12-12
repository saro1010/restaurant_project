
# 🍽️ Restaurant Management System  
A simple command-line application for managing restaurant operations using **Python** and **PostgreSQL**.

This project allows restaurant staff to manage menus, tables, orders, and order details through a clean and interactive CLI interface.

---

## 🚀 Features

### ✔️ Menu Management
- Add new menu items  
- View menu items  
- Update item details  
- Delete items  

### ✔️ Table Management
- Add new tables  
- View all tables  
- Update table status (Available / Reserved / Occupied)  
- Delete a table  

### ✔️ Order Management
- Create a new order for a table  
- Add items to orders  
- Calculate total bill  
- View all orders  
- View order details  

---

## 🗂️ Project Structure

```
restaurant_project/
│
├── app.py # Main application file
├── schema.sql # Database schema (CREATE TABLE statements)
├── requirements.txt # Python dependencies
├── .gitignore # Ignore venv and other unnecessary files
└── venv/ # Virtual environment (ignored)
```
----

## 🚀 How to Run the Project



##### 1. First, create a PostgreSQL database (for example: restaurant_db) and run the provided SQL script to create the tables:

```
CREATE TABLE menu_items (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    price DECIMAL NOT NULL
);

CREATE TABLE tables (
    id SERIAL PRIMARY KEY,
    table_number INTEGER UNIQUE NOT NULL,
    status VARCHAR NOT NULL DEFAULT 'available'
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    table_id INTEGER REFERENCES tables(id),
    order_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR NOT NULL
);

CREATE TABLE order_details (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id),
    item_id INTEGER REFERENCES menu_items(id),
    quantity INTEGER NOT NULL
);

```
----

#### 2. Configure database connection


```
psycopg2.connect(
    dbname="restaurant_db",
    user="postgres",
    password="YOUR_PASSWORD",
    host="localhost"
)
```
----

##### Replace YOUR_PASSWORD with your PostgreSQL password.


#### 3. Install required dependencies

```
pip install psycopg2
```
---

#### 4.Use the menu-driven interface<

##### **The program will start with a text-based menu where you can:**

+ **Manage menu items**

+ **Manage tables**

+ **Create and manage orders**

+ **View daily sales reports**
---
## 🛠️ Technologies Used

- **Python 3.x**
- **PostgreSQL**
- **psycopg2-binary** for database connection
- **Git / GitHub**

