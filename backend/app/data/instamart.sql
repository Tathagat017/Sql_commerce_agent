-- Schema
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS prices;

CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL
);

CREATE TABLE prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    price REAL NOT NULL,
    discount REAL NOT NULL,
    in_stock INTEGER NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY(product_id) REFERENCES products(id)
);

-- Insert products
INSERT INTO products (name, category) VALUES
('Sweater', 'clothes'),
('Jacket', 'clothes'),
('Orange', 'fruits'),
('Pineapple', 'fruits'),
('Cabbage', 'vegetables'),
('Onion', 'vegetables'),
('Curd', 'dairy'),
('Yogurt', 'dairy');

-- Insert prices
INSERT INTO prices (product_id, price, discount, in_stock, updated_at) VALUES
(1, 1099.0, 30.0, 1, '2025-07-24 14:01:00'),
(2, 1499.0, 20.0, 0, '2025-07-24 14:01:00'),
(3, 60.0, 0.0, 1, '2025-07-24 14:01:00'),
(4, 90.0, 10.0, 1, '2025-07-24 14:01:00'),
(5, 28.0, 5.0, 1, '2025-07-24 14:01:00'),
(6, 34.0, 0.0, 0, '2025-07-24 14:01:00'),
(7, 40.0, 15.0, 1, '2025-07-24 14:01:00'),
(8, 70.0, 8.0, 1, '2025-07-24 14:01:00');
