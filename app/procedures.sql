DROP PROCEDURE IF EXISTS CreateSalesTransaction;

DELIMITER //

CREATE PROCEDURE CreateSalesTransaction (
    IN p_Type VARCHAR(20),
    IN p_MemberEmail VARCHAR(100),
    IN p_EmployeeEmail VARCHAR(100),
    IN p_PayMethod VARCHAR(20),
    IN p_Items JSON
)
BEGIN
    DECLARE v_TransactionID BIGINT UNSIGNED;
    DECLARE v_Total DECIMAL(10, 2) DEFAULT 0.0;
    DECLARE v_MemberID BIGINT UNSIGNED;
    DECLARE v_EmployeeID BIGINT UNSIGNED;

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    SELECT ID
    INTO v_MemberID
    FROM Member
    WHERE Member.Email = p_MemberEmail;

    SELECT ID
    INTO v_EmployeeID
    FROM Employee
    WHERE Employee.Email = p_EmployeeEmail

    IF v_EmployeeID IS NULL THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Employee not found';
    END IF;

    INSERT INTO SalesTransaction
        (Type, MemberID, EmployeeID, PayMethod)
    VALUES
        (p_Type, v_MemberID, v_EmployeeID, p_PayMethod);

    SET v_TransactionID = LAST_INSERT_ID();

    INSERT INTO TransactionItem
        (SalesTransactionID, ProductID, Quantity, Total)
    SELECT
        v_TransactionID,
        item.ProductID,
        item.Quantity,
        item.Quantity * Product.Price
    FROM JSON_TABLE(
        p_Items,
        '$[*]' COLUMNS (
            ProductID BIGINT UNSIGNED PATH '$.product_id',
            Quantity INT UNSIGNED PATH '$.quantity'
        )
    ) AS item
    JOIN Product ON Product.ID = item.ProductID;

    UPDATE Product
    JOIN JSON_TABLE(
        p_Items,
        '$[*]' COLUMNS (
            ProductID BIGINT UNSIGNED PATH '$.product_id',
            Quantity INT UNSIGNED PATH '$.quantity'
        )
    ) AS item ON Product.ID = item.ProductID
    SET Product.Stock = Product.Stock - item.Quantity;

    SELECT SUM(Total)
    INTO v_Total
    FROM TransactionItem
    WHERE SalesTransactionID = v_TransactionID;

    UPDATE SalesTransaction
    SET Total = v_Total
    WHERE ID = v_TransactionID;

    COMMIT;
END //

DELIMITER ;