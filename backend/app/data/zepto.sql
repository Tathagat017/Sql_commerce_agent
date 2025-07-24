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
    in_stock INTEGER NOT NULL,        -- 1 = in stock, 0 = out
    updated_at TEXT NOT NULL,
    FOREIGN KEY(product_id) REFERENCES products(id)
);

-- Insert products
INSERT INTO products (name, category) VALUES
('T-shirt', 'clothes'),
('Jeans', 'clothes'),
('Banana', 'fruits'),
('Apple', 'fruits'),
('Spinach', 'vegetables'),
('Tomato', 'vegetables'),
('Milk', 'dairy'),
('Cheese', 'dairy');

-- Insert prices
INSERT INTO prices (product_id, price, discount, in_stock, updated_at) VALUES
(1, 299.0, 20.0, 1, '2025-07-24 14:01:00'),
(2, 799.0, 15.0, 1, '2025-07-24 14:01:00'),
(3, 30.0, 0.0, 1, '2025-07-24 14:01:00'),
(4, 110.0, 5.0, 0, '2025-07-24 14:01:00'),
(5, 40.0, 10.0, 1, '2025-07-24 14:01:00'),
(6, 45.0, 0.0, 0, '2025-07-24 14:01:00'),
(7, 60.0, 10.0, 1, '2025-07-24 14:01:00'),
(8, 240.0, 25.0, 1, '2025-07-24 14:01:00');
