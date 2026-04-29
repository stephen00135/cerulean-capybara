CREATE DATABASE IF NOT EXISTS cerulean_capybara;
USE cerulean_capybara;

CREATE TABLE IF NOT EXISTS Game (
    ID SERIAL,
    Title VARCHAR(50) NOT NULL,
    Platform VARCHAR(30) NOT NULL,
    ReleaseYear YEAR NOT NULL,
    Genre VARCHAR(30),
    Publisher VARCHAR(50),
    Developer VARCHAR(50),
    Rating ENUM('E', 'E10+', 'T', 'M', 'AO', 'RP'),

    UNIQUE (Title, Platform, ReleaseYear)
);

CREATE TABLE IF NOT EXISTS Console (
    ID SERIAL,
    Name VARCHAR(30) NOT NULL,
    Model VARCHAR(50) NOT NULL,
    Platform VARCHAR(30) NOT NULL,
    ReleaseYear YEAR,
    DiscontinueYear YEAR,

    UNIQUE (Name, Model)
);

CREATE TABLE IF NOT EXISTS Member (
    ID SERIAL,
    FirstName VARCHAR(30) NOT NULL,
    LastName VARCHAR(30) NOT NULL,
    Email VARCHAR(100) NOT NULL UNIQUE,
    Points INT UNSIGNED DEFAULT 0 NOT NULL,
    JoinDate DATE NOT NULL DEFAULT (CURRENT_DATE)
);

CREATE TABLE IF NOT EXISTS Employee (
    ID SERIAL,
    FirstName VARCHAR(30) NOT NULL,
    LastName VARCHAR(30) NOT NULL,
    Phone VARCHAR(15) NOT NULL UNIQUE,
    Email VARCHAR(100) NOT NULL UNIQUE,
    Status ENUM('active', 'terminated') DEFAULT 'active' NOT NULL,
    Title VARCHAR(50),
    HourlyWage DECIMAL(6, 2),
    ManagerID BIGINT UNSIGNED,

    FOREIGN KEY (ManagerID) REFERENCES Employee(ID)
);

CREATE TABLE IF NOT EXISTS SalesTransaction (
    ID SERIAL,
    Type ENUM('sale', 'return') NOT NULL,
    MemberID BIGINT UNSIGNED,
    EmployeeID BIGINT UNSIGNED NOT NULL,
    Date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    Total DECIMAL(10, 2) NOT NULL DEFAULT 0.0,
    PayMethod ENUM('credit', 'cash', 'debit') NOT NULL,

    FOREIGN KEY (MemberID) REFERENCES Member(ID),
    FOREIGN KEY (EmployeeID) REFERENCES Employee(ID)
);

CREATE TABLE IF NOT EXISTS Product (
    ID SERIAL,
    SKU VARCHAR(50) NOT NULL UNIQUE,
    Name VARCHAR(50) NOT NULL,
    Price DECIMAL(10, 2) NOT NULL,
    ProductCondition ENUM('new', 'used') NOT NULL DEFAULT 'new',
    Stock INT UNSIGNED NOT NULL DEFAULT 0,
    Brand VARCHAR(50) DEFAULT NULL,
    GameID BIGINT UNSIGNED DEFAULT NULL,
    ConsoleID BIGINT UNSIGNED DEFAULT NULL,

    FOREIGN KEY (GameID) REFERENCES Game(ID),
    FOREIGN KEY (ConsoleID) REFERENCES Console(ID)
);

CREATE TABLE IF NOT EXISTS TransactionItem (
    ID SERIAL,
    SalesTransactionID BIGINT UNSIGNED NOT NULL,
    ProductID BIGINT UNSIGNED NOT NULL,
    Quantity INT UNSIGNED NOT NULL,
    Total DECIMAL(10, 2) NOT NULL,

    UNIQUE (SalesTransactionID, ProductID),

    FOREIGN KEY (SalesTransactionID) REFERENCES SalesTransaction(ID),
    FOREIGN KEY (ProductID) REFERENCES Product(ID)
);
