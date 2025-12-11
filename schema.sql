-- ============================
-- Restaurant Management System
-- Database Schema
-- ============================

-- ----------------------------
-- Table: menu_items
-- ----------------------------
CREATE TABLE menu_items (
    item_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(255),
    price DECIMAL(10,2) NOT NULL
);

-- ----------------------------
-- Table: tables
-- ----------------------------
CREATE TABLE tables (
    table_id SERIAL PRIMARY KEY,
    capacity INT NOT NULL,
    status VARCHAR(20) NOT NULL
);

-- ----------------------------
-- Table: orders
-- ----------------------------
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    table_id INT NOT NULL,
    order_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_price DECIMAL(10,2),
    FOREIGN KEY (table_id) REFERENCES tables(table_id)
);

-- ----------------------------
-- Table: order_details
-- ----------------------------
CREATE TABLE order_details (
    detail_id SERIAL PRIMARY KEY,
    order_id INT NOT NULL,
    item_id INT NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (item_id) REFERENCES menu_items(item_id)
);
