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

    /*
    Find IDs from email
    */
    SELECT ID
    INTO v_MemberID
    FROM Member
    WHERE Member.Email = p_MemberEmail;

    SELECT ID
    INTO v_EmployeeID
    FROM Employee
    WHERE Employee.Email = p_EmployeeEmail
      AND Employee.Status = 'active';

    /*
    Check if employee exists and is active
    */
    IF v_EmployeeID IS NULL THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Employee not found or inactive';
    END IF;

    /*
    Insert transaction
    */
    INSERT INTO SalesTransaction
        (Type, MemberID, EmployeeID, PayMethod)
    VALUES
        (p_Type, v_MemberID, v_EmployeeID, p_PayMethod);

    SET v_TransactionID = LAST_INSERT_ID();

    /*
    Insert line items
    */
    INSERT INTO TransactionItem
        (SalesTransactionID, ProductID, Quantity, Total)
    SELECT
        v_TransactionID,
        Product.ID,
        item.Quantity,
        item.Quantity * Product.Price
    FROM JSON_TABLE(
        p_Items,
        '$[*]' COLUMNS (
            SKU VARCHAR(50) PATH '$.sku',
            Quantity INT UNSIGNED PATH '$.quantity'
        )
    ) AS item
    JOIN Product ON Product.SKU = item.SKU;

    /*
    Update quantity from sku
    */
    UPDATE Product
    JOIN JSON_TABLE(
        p_Items,
        '$[*]' COLUMNS (
            SKU VARCHAR(50) PATH '$.sku',
            Quantity INT UNSIGNED PATH '$.quantity'
        )
    ) AS item ON Product.SKU = item.SKU
    SET Product.Stock = CASE
        WHEN p_Type = 'sale' THEN Product.Stock - item.Quantity
        WHEN p_Type IN ('return', 'trade') THEN Product.Stock + item.Quantity
        ELSE Product.Stock
    END;

    /*
    Record transaction total
    */
    SELECT SUM(Total)
    INTO v_Total
    FROM TransactionItem
    WHERE SalesTransactionID = v_TransactionID;

    UPDATE SalesTransaction
    SET Total = v_Total
    WHERE ID = v_TransactionID;

    /*
    Add points if member sale
    */
    IF p_Type = 'sale' AND v_MemberID IS NOT NULL THEN
        UPDATE Member
        SET Points = Points + FLOOR(v_Total*10)
        WHERE ID = v_MemberID;
    END IF;

    COMMIT;

    SELECT v_TransactionID as SalesTransactionID;
END //

DELIMITER ;
