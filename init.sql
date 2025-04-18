INSERT INTO users (id, username, password, role)
VALUES (1, 'admin', 'adminpass', 'admin');

INSERT INTO products (id, name, price)
VALUES
  (1, 'Apple', 1.0),
  (2, 'Banana', 0.5);

INSERT INTO inventory_entries (product_id, quantity, expiration_date)
VALUES
  (1, 10, NOW() + INTERVAL '2 days'),
  (2, 3, NOW() + INTERVAL '5 days');
