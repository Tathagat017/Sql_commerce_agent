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
('Shirt', 'clothes'),
('Shorts', 'clothes'),
('Mango', 'fruits'),
('Grapes', 'fruits'),
('Carrot', 'vegetables'),
('Potato', 'vegetables'),
('Butter', 'dairy'),
('Paneer', 'dairy');

-- Insert prices
INSERT INTO prices (product_id, price, discount, in_stock, updated_at) VALUES
(1, 399.0, 25.0, 1, '2025-07-24 14:01:00'),
(2, 350.0, 10.0, 0, '2025-07-24 14:01:00'),
(3, 80.0, 5.0, 1, '2025-07-24 14:01:00'),
(4, 120.0, 15.0, 1, '2025-07-24 14:01:00'),
(5, 35.0, 0.0, 1, '2025-07-24 14:01:00'),
(6, 30.0, 0.0, 0, '2025-07-24 14:01:00'),
(7, 90.0, 12.0, 1, '2025-07-24 14:01:00'),
(8, 210.0, 18.0, 1, '2025-07-24 14:01:00');
