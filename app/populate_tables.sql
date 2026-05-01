-- =====================
-- GAME DATA
-- =====================
INSERT INTO Game (Title, Platform, ReleaseYear, Genre, Publisher, Developer, Rating) VALUES
('The Legend of Zelda: Breath of the Wild', 'Switch', 2017, 'Action-Adventure', 'Nintendo', 'Nintendo EPD', 'E10+'),
('God of War', 'PS4', 2018, 'Action', 'Sony Interactive Entertainment', 'Santa Monica Studio', 'M'),
('Halo Infinite', 'Xbox Series X', 2021, 'Shooter', 'Xbox Game Studios', '343 Industries', 'T'),
('Minecraft', 'Multi-platform', 2011, 'Sandbox', 'Mojang', 'Mojang Studios', 'E'),
('Elden Ring', 'PS5', 2022, 'RPG', 'Bandai Namco', 'FromSoftware', 'M');

-- =====================
-- CONSOLE DATA
-- =====================
INSERT INTO Console (Name, Model, Platform, ReleaseYear, DiscontinueYear) VALUES
('Nintendo Switch', 'Standard', 'Switch', 2017, NULL),
('PlayStation 4', 'Slim', 'PS4', 2016, NULL),
('Xbox Series X', 'Standard', 'Xbox Series X', 2020, NULL),
('PlayStation 5', 'Disc Edition', 'PS5', 2020, NULL);

-- =====================
-- MEMBER DATA
-- =====================
INSERT INTO Member (FirstName, LastName, Email, Points, JoinDate) VALUES
('Alice', 'Johnson', 'alice@example.com', 120, '2023-01-15'),
('Bob', 'Smith', 'bob@example.com', 75, '2023-03-10'),
('Charlie', 'Brown', 'charlie@example.com', 200, '2022-11-05');

-- =====================
-- EMPLOYEE DATA
-- =====================
INSERT INTO Employee (FirstName, LastName, Phone, Email, Status, Title, HourlyWage, ManagerID) VALUES
('Dana', 'White', '555-111-2222', 'dana@example.com', 'active', 'Manager', 30.00, NULL),
('Evan', 'Taylor', '555-333-4444', 'evan@example.com', 'active', 'Sales Associate', 15.50, 1),
('Fiona', 'Green', '555-555-6666', 'fiona@example.com', 'active', 'Sales Associate', 15.50, 1),
('George', 'Black', '555-777-8888', 'george@example.com', 'terminated', 'Sales Associate', 14.00, 1);

-- =====================
-- PRODUCT DATA
-- =====================
INSERT INTO Product (SKU, Name, Price, ProductCondition, Stock, Brand, GameID, ConsoleID) VALUES
('1', 'Zelda BOTW Copy', 59.99, 'new', 20, 'Nintendo', 1, NULL),
('2', 'God of War Copy', 39.99, 'used', 10, 'Sony', 2, NULL),
('3', 'Halo Infinite Copy', 49.99, 'new', 15, 'Microsoft', 3, NULL),
('4', 'Minecraft Copy', 29.99, 'new', 25, 'Mojang', 4, NULL),
('5', 'Elden Ring Copy', 69.99, 'new', 12, 'Bandai Namco', 5, NULL),
('6', 'Nintendo Switch Console', 299.99, 'new', 8, 'Nintendo', NULL, 1),
('7', 'PS4 Slim Console', 249.99, 'used', 5, 'Sony', NULL, 2),
('8', 'Xbox Series X Console', 499.99, 'new', 6, 'Microsoft', NULL, 3),
('9', 'PS5 Console', 499.99, 'new', 4, 'Sony', NULL, 4);

-- =====================
-- SALES TRANSACTION DATA (MANUAL INSERT)
-- =====================
INSERT INTO SalesTransaction (Type, MemberID, EmployeeID, Date, Total, PayMethod) VALUES
('sale', 1, 2, NOW(), 59.99, 'credit'),
('sale', 2, 3, NOW(), 29.99, 'cash');

-- =====================
-- TRANSACTION ITEMS
-- =====================
INSERT INTO TransactionItem (SalesTransactionID, ProductID, Quantity, Total) VALUES
(1, 1, 1, 59.99),
(2, 4, 1, 29.99);

-- =====================
-- EXAMPLE STORED PROCEDURE CALL
-- =====================
CALL CreateSalesTransaction(
    'sale',
    'alice@example.com',
    'evan@example.com',
    'credit',
    JSON_ARRAY(
        JSON_OBJECT('product_id', 1, 'quantity', 1)
    )
);