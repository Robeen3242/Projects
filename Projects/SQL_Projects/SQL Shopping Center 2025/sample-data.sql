PRAGMA foreign_keys = on;
-- Converted data for new schema
-- Generated on 2025-11-04 06:35:29 UTC

-- users
INSERT INTO users (uid, pwd, role) VALUES (101, 'pwd101', 'customer');
INSERT INTO users (uid, pwd, role) VALUES (102, 'pwd102', 'customer');
INSERT INTO users (uid, pwd, role) VALUES (103, 'pwd103', 'customer');
INSERT INTO users (uid, pwd, role) VALUES (104, 'pwd104', 'customer');
INSERT INTO users (uid, pwd, role) VALUES (105, 'pwd105', 'customer');
INSERT INTO users (uid, pwd, role) VALUES (106, 'pwd106', 'customer');
INSERT INTO users (uid, pwd, role) VALUES (107, 'pwd107', 'customer');
INSERT INTO users (uid, pwd, role) VALUES (108, 'pwd108', 'customer');
INSERT INTO users (uid, pwd, role) VALUES (109, 'pwd109', 'customer');
INSERT INTO users (uid, pwd, role) VALUES (110, 'pwd110', 'customer');
INSERT INTO users (uid, pwd, role) VALUES (111, 'pwd111', 'customer');
INSERT INTO users (uid, pwd, role) VALUES (112, 'pwd112', 'customer');
INSERT INTO users (uid, pwd, role) VALUES (999, 'adminpwd', 'sales');

-- customers
INSERT INTO customers (cid, name, email) VALUES (101, 'John Smith', 'john@example.com');
INSERT INTO customers (cid, name, email) VALUES (102, 'Jane Doe', 'jane@example.com');
INSERT INTO customers (cid, name, email) VALUES (103, 'Alice Johnson', 'alice@example.com');
INSERT INTO customers (cid, name, email) VALUES (104, 'Bob Brown', 'bob@example.com');
INSERT INTO customers (cid, name, email) VALUES (105, 'Charlie Davis', 'charlie@example.com');
INSERT INTO customers (cid, name, email) VALUES (106, 'Eve Adams', 'eve@example.com');
INSERT INTO customers (cid, name, email) VALUES (107, 'Oscar Martinez', 'oscar@example.com');
INSERT INTO customers (cid, name, email) VALUES (108, 'Gary White', 'gary@example.com');
INSERT INTO customers (cid, name, email) VALUES (109, 'Helen Taylor', 'helen@example.com');
INSERT INTO customers (cid, name, email) VALUES (110, 'Sam Wilson', 'sam@example.com');
INSERT INTO customers (cid, name, email) VALUES (111, 'Jack Reed', 'jack@example.com');
INSERT INTO customers (cid, name, email) VALUES (112, 'Ian Lee', 'ian@example.com');

-- products
INSERT INTO products (pid, name, category, price, stock_count, descr) VALUES (201, 'Smartphone', 'Electronics', 699.0, 50, 'Latest smartphone');
INSERT INTO products (pid, name, category, price, stock_count, descr) VALUES (202, 'Laptop', 'electronics', 999.0, 40, 'High performance laptop');
INSERT INTO products (pid, name, category, price, stock_count, descr) VALUES (203, 'Tablet', 'ElectrOniCS', 499.0, 60, 'Portable tablet device');
INSERT INTO products (pid, name, category, price, stock_count, descr) VALUES (204, 'Bookcase', 'Home', 120.0, 30, 'Wooden bookcase');
INSERT INTO products (pid, name, category, price, stock_count, descr) VALUES (205, 'Toy Car', 'Toys', 30.0, 100, 'Toy car for kids');
INSERT INTO products (pid, name, category, price, stock_count, descr) VALUES (206, 'Headphones', 'Electronics', 199.0, 70, 'Noise cancelling headphones');
INSERT INTO products (pid, name, category, price, stock_count, descr) VALUES (207, 'Smartwatch', 'electronics', 250.0, 45, 'Fitness smartwatch');
INSERT INTO products (pid, name, category, price, stock_count, descr) VALUES (208, 'Camera', 'Electronics', 450.0, 25, 'Digital camera');
INSERT INTO products (pid, name, category, price, stock_count, descr) VALUES (209, 'Coffee Maker', 'Home Appliances', 80.0, 50, 'Coffee maker machine');
INSERT INTO products (pid, name, category, price, stock_count, descr) VALUES (210, 'Drone', 'electronics', 300.0, 20, 'Quadcopter drone');

-- sessions
INSERT INTO sessions (cid, sessionNo, start_time, end_time) VALUES (101, 1, '2025-09-01 09:00:00', '2025-09-01 12:00:00');
INSERT INTO sessions (cid, sessionNo, start_time, end_time) VALUES (101, 2, '2025-08-25 09:00:00', '2025-08-25 10:00:00');
INSERT INTO sessions (cid, sessionNo, start_time, end_time) VALUES (102, 1, '2025-09-10 11:00:00', '2025-09-10 12:00:00');
INSERT INTO sessions (cid, sessionNo, start_time, end_time) VALUES (102, 2, '2025-08-15 08:00:00', '2025-08-15 09:00:00');
INSERT INTO sessions (cid, sessionNo, start_time, end_time) VALUES (103, 1, '2025-09-05 13:00:00', '2025-09-05 14:00:00');
INSERT INTO sessions (cid, sessionNo, start_time, end_time) VALUES (103, 2, '2025-06-05 08:00:00', '2025-06-05 09:00:00');
INSERT INTO sessions (cid, sessionNo, start_time, end_time) VALUES (104, 1, '2025-09-10 15:00:00', '2025-09-10 17:00:00');
INSERT INTO sessions (cid, sessionNo, start_time, end_time) VALUES (104, 2, '2025-08-01 10:00:00', '2025-08-01 11:00:00');
INSERT INTO sessions (cid, sessionNo, start_time, end_time) VALUES (104, 3, '2025-07-07 10:00:00', '2025-07-07 11:00:00');
INSERT INTO sessions (cid, sessionNo, start_time, end_time) VALUES (104, 4, '2024-12-20 10:00:00', '2024-12-20 11:00:00');
INSERT INTO sessions (cid, sessionNo, start_time, end_time) VALUES (105, 1, '2025-08-28 10:00:00', '2025-08-28 10:45:00');
INSERT INTO sessions (cid, sessionNo, start_time, end_time) VALUES (105, 2, '2025-08-30 09:00:00', '2025-08-30 11:00:00');
INSERT INTO sessions (cid, sessionNo, start_time, end_time) VALUES (106, 1, '2025-07-05 10:00:00', '2025-07-05 11:00:00');
INSERT INTO sessions (cid, sessionNo, start_time, end_time) VALUES (106, 2, '2024-10-25 09:30:00', '2024-10-25 10:30:00');
INSERT INTO sessions (cid, sessionNo, start_time, end_time) VALUES (107, 1, '2025-09-15 14:00:00', '2025-09-15 15:00:00');
INSERT INTO sessions (cid, sessionNo, start_time, end_time) VALUES (108, 1, '2025-09-03 10:00:00', '2025-09-03 11:00:00');
INSERT INTO sessions (cid, sessionNo, start_time, end_time) VALUES (108, 2, '2025-09-04 11:00:00', '2025-09-04 12:00:00');
INSERT INTO sessions (cid, sessionNo, start_time, end_time) VALUES (109, 1, '2025-08-27 10:00:00', '2025-08-27 10:45:00');
INSERT INTO sessions (cid, sessionNo, start_time, end_time) VALUES (109, 2, '2025-07-15 12:00:00', '2025-07-15 12:30:00');
INSERT INTO sessions (cid, sessionNo, start_time, end_time) VALUES (110, 1, '2024-11-11 09:00:00', '2024-11-11 10:00:00');
INSERT INTO sessions (cid, sessionNo, start_time, end_time) VALUES (110, 2, '2025-09-18 10:00:00', '2025-09-18 11:30:00');
INSERT INTO sessions (cid, sessionNo, start_time, end_time) VALUES (111, 1, '2025-09-12 16:00:00', '2025-09-12 17:00:00');
INSERT INTO sessions (cid, sessionNo, start_time, end_time) VALUES (112, 1, '2025-05-10 08:00:00', '2025-05-10 08:30:00');

-- orders (merged with orderSessions to include cid and sessionNo)
INSERT INTO orders (ono, cid, sessionNo, odate, shipping_address) VALUES (301, '101', '1', '2025-09-01', '123 Main St, Edmonton');
INSERT INTO orders (ono, cid, sessionNo, odate, shipping_address) VALUES (302, '102', '2', '2025-08-15', '555 Elm St, edmonton');
INSERT INTO orders (ono, cid, sessionNo, odate, shipping_address) VALUES (303, '103', '2', '2025-06-05', 'Calgary, Alberta');
INSERT INTO orders (ono, cid, sessionNo, odate, shipping_address) VALUES (304, '104', '4', '2024-12-20', '123 Main St, Edmonton');
INSERT INTO orders (ono, cid, sessionNo, odate, shipping_address) VALUES (305, '104', '3', '2025-07-07', 'Vancouver, BC');
INSERT INTO orders (ono, cid, sessionNo, odate, shipping_address) VALUES (306, '110', '1', '2024-11-11', 'Edmonton, AB');
INSERT INTO orders (ono, cid, sessionNo, odate, shipping_address) VALUES (307, '105', '2', '2025-08-30', 'Edmonton AB');
INSERT INTO orders (ono, cid, sessionNo, odate, shipping_address) VALUES (308, '110', '2', '2025-09-18', 'Calgary');
INSERT INTO orders (ono, cid, sessionNo, odate, shipping_address) VALUES (309, '106', '2', '2024-10-25', 'Calgary');
INSERT INTO orders (ono, cid, sessionNo, odate, shipping_address) VALUES (310, '106', '1', '2025-07-05', 'Edmonton');
INSERT INTO orders (ono, cid, sessionNo, odate, shipping_address) VALUES (311, '112', '1', '2025-05-10', 'Calgary');

-- orderlines (discount removed)
INSERT INTO orderlines (ono, lineNo, pid, qty, uprice) VALUES (301.0, 1.0, 201.0, 1.0, 699.0);
INSERT INTO orderlines (ono, lineNo, pid, qty, uprice) VALUES (301.0, 2.0, 204.0, 1.0, 120.0);
INSERT INTO orderlines (ono, lineNo, pid, qty, uprice) VALUES (302.0, 1.0, 201.0, 1.0, 699.0);
INSERT INTO orderlines (ono, lineNo, pid, qty, uprice) VALUES (302.0, 2.0, 206.0, 1.0, 199.0);
INSERT INTO orderlines (ono, lineNo, pid, qty, uprice) VALUES (302.0, 3.0, 204.0, 1.0, 120.0);
INSERT INTO orderlines (ono, lineNo, pid, qty, uprice) VALUES (303.0, 1.0, 201.0, 1.0, 699.0);
INSERT INTO orderlines (ono, lineNo, pid, qty, uprice) VALUES (303.0, 2.0, 203.0, 1.0, 499.0);
INSERT INTO orderlines (ono, lineNo, pid, qty, uprice) VALUES (303.0, 3.0, 205.0, 2.0, 30.0);
INSERT INTO orderlines (ono, lineNo, pid, qty, uprice) VALUES (303.0, 4.0, 208.0, 1.0, 450.0);
INSERT INTO orderlines (ono, lineNo, pid, qty, uprice) VALUES (303.0, 5.0, 202.0, 1.0, 999.0);
INSERT INTO orderlines (ono, lineNo, pid, qty, uprice) VALUES (304.0, 1.0, 204.0, 1.0, 120.0);
INSERT INTO orderlines (ono, lineNo, pid, qty, uprice) VALUES (304.0, 2.0, 205.0, 2.0, 30.0);
INSERT INTO orderlines (ono, lineNo, pid, qty, uprice) VALUES (304.0, 3.0, 209.0, 1.0, 80.0);
INSERT INTO orderlines (ono, lineNo, pid, qty, uprice) VALUES (304.0, 4.0, 206.0, 1.0, 199.0);
INSERT INTO orderlines (ono, lineNo, pid, qty, uprice) VALUES (305.0, 1.0, 201.0, 1.0, 699.0);
INSERT INTO orderlines (ono, lineNo, pid, qty, uprice) VALUES (305.0, 2.0, 206.0, 1.0, 199.0);
INSERT INTO orderlines (ono, lineNo, pid, qty, uprice) VALUES (305.0, 3.0, 208.0, 1.0, 450.0);
INSERT INTO orderlines (ono, lineNo, pid, qty, uprice) VALUES (305.0, 4.0, 207.0, 1.0, 250.0);
INSERT INTO orderlines (ono, lineNo, pid, qty, uprice) VALUES (306.0, 1.0, 209.0, 1.0, 80.0);
INSERT INTO orderlines (ono, lineNo, pid, qty, uprice) VALUES (306.0, 2.0, 204.0, 1.0, 120.0);
INSERT INTO orderlines (ono, lineNo, pid, qty, uprice) VALUES (307.0, 1.0, 201.0, 1.0, 699.0);
INSERT INTO orderlines (ono, lineNo, pid, qty, uprice) VALUES (307.0, 2.0, 202.0, 1.0, 999.0);
INSERT INTO orderlines (ono, lineNo, pid, qty, uprice) VALUES (307.0, 3.0, 203.0, 1.0, 499.0);
INSERT INTO orderlines (ono, lineNo, pid, qty, uprice) VALUES (307.0, 4.0, 208.0, 1.0, 450.0);
INSERT INTO orderlines (ono, lineNo, pid, qty, uprice) VALUES (307.0, 5.0, 206.0, 1.0, 199.0);
INSERT INTO orderlines (ono, lineNo, pid, qty, uprice) VALUES (308.0, 1.0, 201.0, 1.0, 699.0);
INSERT INTO orderlines (ono, lineNo, pid, qty, uprice) VALUES (308.0, 2.0, 202.0, 1.0, 999.0);
INSERT INTO orderlines (ono, lineNo, pid, qty, uprice) VALUES (308.0, 3.0, 204.0, 1.0, 120.0);
INSERT INTO orderlines (ono, lineNo, pid, qty, uprice) VALUES (308.0, 4.0, 209.0, 1.0, 80.0);
INSERT INTO orderlines (ono, lineNo, pid, qty, uprice) VALUES (309.0, 1.0, 201.0, 1.0, 699.0);
INSERT INTO orderlines (ono, lineNo, pid, qty, uprice) VALUES (309.0, 2.0, 204.0, 1.0, 120.0);
INSERT INTO orderlines (ono, lineNo, pid, qty, uprice) VALUES (309.0, 3.0, 205.0, 2.0, 30.0);
INSERT INTO orderlines (ono, lineNo, pid, qty, uprice) VALUES (309.0, 4.0, 206.0, 1.0, 199.0);
INSERT INTO orderlines (ono, lineNo, pid, qty, uprice) VALUES (310.0, 1.0, 201.0, 1.0, 699.0);
INSERT INTO orderlines (ono, lineNo, pid, qty, uprice) VALUES (310.0, 2.0, 204.0, 1.0, 120.0);
INSERT INTO orderlines (ono, lineNo, pid, qty, uprice) VALUES (311.0, 1.0, 201.0, 1.0, 699.0);

-- viewedProduct
INSERT INTO viewedProduct (cid, sessionNo, ts, pid) VALUES (101, 1, '2025-09-01 09:10:00', 201);
INSERT INTO viewedProduct (cid, sessionNo, ts, pid) VALUES (101, 1, '2025-09-01 09:12:01', 204);
INSERT INTO viewedProduct (cid, sessionNo, ts, pid) VALUES (101, 2, '2025-08-25 09:10:00', 202);
INSERT INTO viewedProduct (cid, sessionNo, ts, pid) VALUES (101, 2, '2025-08-25 09:30:03', 201);
INSERT INTO viewedProduct (cid, sessionNo, ts, pid) VALUES (102, 1, '2025-09-10 11:10:00', 201);
INSERT INTO viewedProduct (cid, sessionNo, ts, pid) VALUES (102, 1, '2025-09-10 11:12:01', 206);
INSERT INTO viewedProduct (cid, sessionNo, ts, pid) VALUES (102, 2, '2025-08-15 08:10:00', 201);
INSERT INTO viewedProduct (cid, sessionNo, ts, pid) VALUES (102, 2, '2025-08-15 08:12:01', 206);
INSERT INTO viewedProduct (cid, sessionNo, ts, pid) VALUES (102, 2, '2025-08-15 08:14:02', 204);
INSERT INTO viewedProduct (cid, sessionNo, ts, pid) VALUES (103, 1, '2025-09-05 13:05:00', 201);
INSERT INTO viewedProduct (cid, sessionNo, ts, pid) VALUES (103, 2, '2025-06-05 08:05:00', 201);
INSERT INTO viewedProduct (cid, sessionNo, ts, pid) VALUES (103, 2, '2025-06-05 08:06:01', 202);
INSERT INTO viewedProduct (cid, sessionNo, ts, pid) VALUES (103, 2, '2025-06-05 08:07:02', 203);
INSERT INTO viewedProduct (cid, sessionNo, ts, pid) VALUES (104, 1, '2025-09-10 15:10:00', 201);
INSERT INTO viewedProduct (cid, sessionNo, ts, pid) VALUES (104, 1, '2025-09-10 16:00:05', 201);
INSERT INTO viewedProduct (cid, sessionNo, ts, pid) VALUES (104, 2, '2025-08-01 10:05:00', 205);
INSERT INTO viewedProduct (cid, sessionNo, ts, pid) VALUES (104, 3, '2025-07-07 10:05:00', 201);
INSERT INTO viewedProduct (cid, sessionNo, ts, pid) VALUES (104, 3, '2025-07-07 10:09:02', 206);
INSERT INTO viewedProduct (cid, sessionNo, ts, pid) VALUES (104, 3, '2025-07-07 10:13:04', 208);
INSERT INTO viewedProduct (cid, sessionNo, ts, pid) VALUES (104, 3, '2025-07-07 10:17:06', 207);
INSERT INTO viewedProduct (cid, sessionNo, ts, pid) VALUES (104, 4, '2024-12-20 10:05:00', 204);
INSERT INTO viewedProduct (cid, sessionNo, ts, pid) VALUES (104, 4, '2024-12-20 10:09:02', 205);
INSERT INTO viewedProduct (cid, sessionNo, ts, pid) VALUES (104, 4, '2024-12-20 10:13:04', 209);
INSERT INTO viewedProduct (cid, sessionNo, ts, pid) VALUES (104, 4, '2024-12-20 10:17:06', 206);
INSERT INTO viewedProduct (cid, sessionNo, ts, pid) VALUES (105, 1, '2025-08-28 10:05:00', 201);
INSERT INTO viewedProduct (cid, sessionNo, ts, pid) VALUES (105, 2, '2025-08-30 09:05:00', 201);
INSERT INTO viewedProduct (cid, sessionNo, ts, pid) VALUES (105, 2, '2025-08-30 09:08:02', 202);
INSERT INTO viewedProduct (cid, sessionNo, ts, pid) VALUES (105, 2, '2025-08-30 09:12:04', 203);
INSERT INTO viewedProduct (cid, sessionNo, ts, pid) VALUES (105, 2, '2025-08-30 09:16:06', 208);
INSERT INTO viewedProduct (cid, sessionNo, ts, pid) VALUES (105, 2, '2025-08-30 09:20:08', 206);
INSERT INTO viewedProduct (cid, sessionNo, ts, pid) VALUES (106, 1, '2025-07-05 10:05:00', 201);
INSERT INTO viewedProduct (cid, sessionNo, ts, pid) VALUES (106, 1, '2025-07-05 10:09:02', 204);
INSERT INTO viewedProduct (cid, sessionNo, ts, pid) VALUES (106, 2, '2024-10-25 09:35:00', 201);
INSERT INTO viewedProduct (cid, sessionNo, ts, pid) VALUES (106, 2, '2024-10-25 09:39:02', 204);
INSERT INTO viewedProduct (cid, sessionNo, ts, pid) VALUES (106, 2, '2024-10-25 09:43:04', 205);
INSERT INTO viewedProduct (cid, sessionNo, ts, pid) VALUES (106, 2, '2024-10-25 09:47:06', 206);
INSERT INTO viewedProduct (cid, sessionNo, ts, pid) VALUES (107, 1, '2025-09-15 14:05:00', 201);
INSERT INTO viewedProduct (cid, sessionNo, ts, pid) VALUES (108, 2, '2025-09-04 11:05:00', 202);
INSERT INTO viewedProduct (cid, sessionNo, ts, pid) VALUES (109, 1, '2025-08-27 10:05:00', 201);
INSERT INTO viewedProduct (cid, sessionNo, ts, pid) VALUES (109, 1, '2025-08-27 10:15:02', 201);
INSERT INTO viewedProduct (cid, sessionNo, ts, pid) VALUES (109, 2, '2025-07-15 12:05:00', 202);
INSERT INTO viewedProduct (cid, sessionNo, ts, pid) VALUES (110, 1, '2024-11-11 09:05:00', 209);
INSERT INTO viewedProduct (cid, sessionNo, ts, pid) VALUES (110, 1, '2024-11-11 09:09:02', 204);
INSERT INTO viewedProduct (cid, sessionNo, ts, pid) VALUES (110, 2, '2025-09-18 10:05:00', 201);
INSERT INTO viewedProduct (cid, sessionNo, ts, pid) VALUES (110, 2, '2025-09-18 10:09:02', 202);
INSERT INTO viewedProduct (cid, sessionNo, ts, pid) VALUES (110, 2, '2025-09-18 10:13:04', 204);
INSERT INTO viewedProduct (cid, sessionNo, ts, pid) VALUES (110, 2, '2025-09-18 10:17:06', 209);

-- search
INSERT INTO search (cid, sessionNo, ts, query) VALUES (101, 1, '2025-09-01 09:30:04', 'Edmonton electronics');
INSERT INTO search (cid, sessionNo, ts, query) VALUES (101, 2, '2025-08-25 09:15:01', 'best laptop deals');
INSERT INTO search (cid, sessionNo, ts, query) VALUES (101, 2, '2025-08-25 09:40:04', 'smartphone vs laptop');
INSERT INTO search (cid, sessionNo, ts, query) VALUES (102, 1, '2025-09-10 11:15:02', 'phone accessories');
INSERT INTO search (cid, sessionNo, ts, query) VALUES (102, 1, '2025-09-10 11:35:05', 'headphones sale');
INSERT INTO search (cid, sessionNo, ts, query) VALUES (103, 1, '2025-09-05 13:25:03', 'tablet vs smartphone');
INSERT INTO search (cid, sessionNo, ts, query) VALUES (104, 1, '2025-09-10 15:25:02', 'latest smartphones');
INSERT INTO search (cid, sessionNo, ts, query) VALUES (104, 2, '2025-08-01 10:20:02', 'toy car kids');
INSERT INTO search (cid, sessionNo, ts, query) VALUES (105, 1, '2025-08-28 10:20:05', 'smartphone deals');
INSERT INTO search (cid, sessionNo, ts, query) VALUES (107, 1, '2025-09-15 14:40:04', 'best smartphones');
INSERT INTO search (cid, sessionNo, ts, query) VALUES (108, 1, '2025-09-03 10:10:00', 'cheap headphones');
INSERT INTO search (cid, sessionNo, ts, query) VALUES (108, 1, '2025-09-03 10:20:01', 'smartphone discount');
INSERT INTO search (cid, sessionNo, ts, query) VALUES (108, 2, '2025-09-04 11:15:01', 'laptop features');
INSERT INTO search (cid, sessionNo, ts, query) VALUES (109, 1, '2025-08-27 10:25:04', 'smartphone reviews');
INSERT INTO search (cid, sessionNo, ts, query) VALUES (109, 2, '2025-07-15 12:10:02', 'laptop battery life');
INSERT INTO search (cid, sessionNo, ts, query) VALUES (111, 1, '2025-09-12 16:10:00', 'upcoming gadgets');
INSERT INTO search (cid, sessionNo, ts, query) VALUES (111, 1, '2025-09-12 16:20:01', 'tech news');
INSERT INTO search (cid, sessionNo, ts, query) VALUES (112, 1, '2025-05-10 08:05:00', 'buy smartphone quickly');

-- cart (aggregated from add2cart)
INSERT INTO cart (cid, sessionNo, pid, qty) VALUES ('101', '1', '201', 1);
INSERT INTO cart (cid, sessionNo, pid, qty) VALUES ('101', '1', '204', 1);
INSERT INTO cart (cid, sessionNo, pid, qty) VALUES ('101', '2', '201', 1);
INSERT INTO cart (cid, sessionNo, pid, qty) VALUES ('101', '2', '202', 1);
INSERT INTO cart (cid, sessionNo, pid, qty) VALUES ('102', '1', '201', 1);
INSERT INTO cart (cid, sessionNo, pid, qty) VALUES ('102', '1', '206', 1);
INSERT INTO cart (cid, sessionNo, pid, qty) VALUES ('102', '2', '201', 1);
INSERT INTO cart (cid, sessionNo, pid, qty) VALUES ('102', '2', '204', 1);
INSERT INTO cart (cid, sessionNo, pid, qty) VALUES ('102', '2', '206', 1);
INSERT INTO cart (cid, sessionNo, pid, qty) VALUES ('103', '1', '201', 2);
INSERT INTO cart (cid, sessionNo, pid, qty) VALUES ('103', '2', '201', 1);
INSERT INTO cart (cid, sessionNo, pid, qty) VALUES ('103', '2', '202', 1);
INSERT INTO cart (cid, sessionNo, pid, qty) VALUES ('103', '2', '203', 1);
INSERT INTO cart (cid, sessionNo, pid, qty) VALUES ('104', '1', '201', 3);
INSERT INTO cart (cid, sessionNo, pid, qty) VALUES ('104', '2', '205', 1);
INSERT INTO cart (cid, sessionNo, pid, qty) VALUES ('104', '3', '201', 1);
INSERT INTO cart (cid, sessionNo, pid, qty) VALUES ('104', '3', '206', 1);
INSERT INTO cart (cid, sessionNo, pid, qty) VALUES ('104', '3', '207', 1);
INSERT INTO cart (cid, sessionNo, pid, qty) VALUES ('104', '3', '208', 1);
INSERT INTO cart (cid, sessionNo, pid, qty) VALUES ('104', '4', '204', 1);
INSERT INTO cart (cid, sessionNo, pid, qty) VALUES ('104', '4', '205', 1);
INSERT INTO cart (cid, sessionNo, pid, qty) VALUES ('104', '4', '206', 1);
INSERT INTO cart (cid, sessionNo, pid, qty) VALUES ('104', '4', '209', 1);
INSERT INTO cart (cid, sessionNo, pid, qty) VALUES ('105', '1', '201', 4);
INSERT INTO cart (cid, sessionNo, pid, qty) VALUES ('105', '2', '201', 1);
INSERT INTO cart (cid, sessionNo, pid, qty) VALUES ('105', '2', '202', 1);
INSERT INTO cart (cid, sessionNo, pid, qty) VALUES ('105', '2', '203', 1);
INSERT INTO cart (cid, sessionNo, pid, qty) VALUES ('105', '2', '206', 1);
INSERT INTO cart (cid, sessionNo, pid, qty) VALUES ('105', '2', '208', 1);
INSERT INTO cart (cid, sessionNo, pid, qty) VALUES ('106', '1', '201', 1);
INSERT INTO cart (cid, sessionNo, pid, qty) VALUES ('106', '1', '204', 1);
INSERT INTO cart (cid, sessionNo, pid, qty) VALUES ('106', '2', '201', 1);
INSERT INTO cart (cid, sessionNo, pid, qty) VALUES ('106', '2', '204', 1);
INSERT INTO cart (cid, sessionNo, pid, qty) VALUES ('106', '2', '205', 1);
INSERT INTO cart (cid, sessionNo, pid, qty) VALUES ('106', '2', '206', 1);
INSERT INTO cart (cid, sessionNo, pid, qty) VALUES ('107', '1', '201', 3);
INSERT INTO cart (cid, sessionNo, pid, qty) VALUES ('109', '1', '201', 2);
INSERT INTO cart (cid, sessionNo, pid, qty) VALUES ('109', '2', '202', 1);
INSERT INTO cart (cid, sessionNo, pid, qty) VALUES ('110', '1', '204', 1);
INSERT INTO cart (cid, sessionNo, pid, qty) VALUES ('110', '1', '209', 1);
INSERT INTO cart (cid, sessionNo, pid, qty) VALUES ('110', '2', '201', 1);
INSERT INTO cart (cid, sessionNo, pid, qty) VALUES ('110', '2', '202', 1);
INSERT INTO cart (cid, sessionNo, pid, qty) VALUES ('110', '2', '204', 1);
INSERT INTO cart (cid, sessionNo, pid, qty) VALUES ('110', '2', '209', 1);

-- Note: the following old tables were present but are not part of the new schema and were not converted:
--   - creditCards
--   - orderSessions
--   - activities
--   - checkout
--   - payment
