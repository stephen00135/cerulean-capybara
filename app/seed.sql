USE cerulean_capybara;

-- Remove only this script's example rows so the seed can be rerun.
DELETE FROM TransactionItem WHERE ID IN (1, 2, 3, 4, 5);
DELETE FROM SalesTransaction WHERE ID IN (1, 2, 3, 4, 5);
DELETE FROM Product WHERE ID IN (201, 202, 203, 204, 205);
DELETE FROM Game WHERE ID IN (401, 402, 403, 404, 405);
DELETE FROM Console WHERE ID IN (301, 302, 303, 304, 305);
DELETE FROM Member WHERE ID IN (1, 2, 3, 4, 5);
DELETE FROM Employee WHERE ID IN (1, 2, 3, 4, 5);

INSERT INTO Game
    (ID, Title, Platform, ReleaseYear, Genre, Publisher, Developer, Rating)
VALUES
    (401, 'Super Mario World', 'SNES', 1990, 'Platformer', 'Nintendo', 'Nintendo', 'E'),
    (402, 'Final Fantasy VII', 'PlayStation', 1997, 'RPG', 'Sony', 'Square', 'T'),
    (403, 'The Legend of Zelda', 'NES', 1986, 'Adventure', 'Nintendo', 'Nintendo', 'E'),
    (404, 'Sonic the Hedgehog', 'Genesis', 1991, 'Platformer', 'Sega', 'Sega', 'E'),
    (405, 'Resident Evil 2', 'PlayStation', 1998, 'Horror', 'Capcom', 'Capcom', 'M');

INSERT INTO Console
    (ID, Name, Model, Platform, ReleaseYear, DiscontinueYear)
VALUES
    (301, 'Nintendo Entertainment System', 'Front Loader', 'NES', 1985, 1995),
    (302, 'Sega Genesis', 'Model 1', 'Genesis', 1989, 1997),
    (303, 'Super Nintendo Entertainment System', 'SNS-001', 'SNES', 1991, 1999),
    (304, 'PlayStation', 'SCPH-1001', 'PlayStation', 1994, 2006),
    (305, 'Nintendo 64', 'NUS-001', 'Nintendo 64', 1996, 2002);

INSERT INTO Member
    (ID, FirstName, LastName, Email, Points, JoinDate)
VALUES
    (1, 'Emily', 'Johnson', 'emily.johnson@email.com', 450, '2022-04-15'),
    (2, 'Kon', 'Keaser', 'kkeaser@mail.com', 12000, '2023-01-08'),
    (3, 'Olivia', 'Davis', 'olivia.d@email.com', 980, '2021-09-21'),
    (4, 'Daniel', 'Miller', 'daniel.m@email.com', 0, '2024-02-02'),
    (5, 'Sophia', 'Wilson', 'sophia.w@email.com', 300, '2023-07-19');

INSERT INTO Employee
    (ID, FirstName, LastName, Phone, Email, Status, Title, HourlyWage, ManagerID)
VALUES
    (1, 'Susy', 'Q', '6812359987', 'susy.q1@gmail.com', 'active', 'Store Manager', 25.00, NULL),
    (2, 'John', 'Doe', '6812313333', 'johndoe1@gmail.com', 'active', 'Sales Associate', 15.50, NULL),
    (3, 'Jane', 'Doe', '3047651234', 'jane.doe1@gmail.com', 'active', 'Sales Associate', 15.00, NULL),
    (4, 'Samuel', 'Brown', '3046921546', 'samuel.brown1@yahoo.com', 'terminated', 'Sales Associate', 16.25, NULL),
    (5, 'Von', 'Veaser', '3045883444', 'vonvon@gmail.com', 'active', 'General Manager', 50.00, NULL);

INSERT INTO Product
    (ID, SKU, Name, Price, ProductCondition, Stock, Brand, GameID, ConsoleID)
VALUES
    (201, 'NES-001', 'Nintendo Entertainment System', 149.99, 'used', 3, 'Nintendo', NULL, 301),
    (202, 'SNES-CTR-001', 'Super Mario World', 39.99, 'used', 5, 'Nintendo', 401, NULL),
    (203, 'GEN-001', 'Sega Genesis', 129.99, 'used', 2, 'Sega', NULL, 302),
    (204, 'PS1-FF7', 'Final Fantasy VII', 59.99, 'used', 4, 'Sony', 402, NULL),
    (205, 'CTRL-N64-001', 'N64 Controller', 24.99, 'new', 10, 'Nintendo', NULL, NULL);

INSERT INTO SalesTransaction
    (ID, Type, MemberID, EmployeeID, Date, Total, PayMethod)
VALUES
    (1, 'sale', 1, 1, '2024-03-01 10:15:00', 149.99, 'credit'),
    (2, 'sale', 2, 2, '2024-03-02 11:30:00', 79.98, 'cash'),
    (3, 'sale', 3, 3, '2024-03-03 14:45:00', 129.99, 'debit'),
    (4, 'return', 4, 1, '2024-03-04 16:20:00', 59.99, 'credit'),
    (5, 'sale', 5, 5, '2024-03-05 18:05:00', 49.98, 'cash');

INSERT INTO TransactionItem
    (ID, SalesTransactionID, ProductID, Quantity, Total)
VALUES
    (1, 1, 201, 1, 149.99),
    (2, 2, 202, 2, 79.98),
    (3, 3, 203, 1, 129.99),
    (4, 4, 204, 1, 59.99),
    (5, 5, 205, 2, 49.98);
