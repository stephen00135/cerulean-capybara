import os
import mysql.connector
from dotenv import load_dotenv
from flask import g, current_app, flash

load_dotenv()

def fetch_employees():
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT
                EmployeeID,
                FirstName,
                LastName,
                Phone,
                Email,
                Status,
                Title,
                HourlyWage
            FROM Employees
            ORDER BY LastName, FirstName
            """
        )
        employees = cursor.fetchall()
        cursor.close()
        return employees
    except mysql.connector.Error:
        flash('Could not load employees from the database.')
        return []

def fetch_products():
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT
                ProductID,
                SKU,
                Name,
                Price,
                ProductCondition,
                Stock,
                Brand
            FROM Products
            ORDER BY Name
            """
        )
        products = cursor.fetchall()
        cursor.close()
        return products
    except mysql.connector.Error:
        flash('Could not load products from the database.')
        return []

def add_employee(form):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO Employees
            (FirstName, LastName, Phone, Email, Status, Title, HourlyWage)
        VALUES
            (%s, %s, %s, %s, %s, %s, %s)
        """,
        (
            form.first_name.data,
            form.last_name.data,
            form.phone.data,
            form.email.data,
            form.status.data,
            form.title.data,
            form.hourly_wage.data,
        ),
    )
    conn.commit()
    cursor.close()

def update_employee_status(form):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE Employees
        SET Status = %s
        WHERE EmployeeID = %s
        """,
        (form.status.data, form.employee_id.data),
    )
    conn.commit()
    cursor.close()

def terminate_employee(form):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE Employees
        SET Status = %s
        WHERE EmployeeID = %s
        """,
        ('terminated', form.employee_id.data),
    )
    conn.commit()
    cursor.close()

def add_product(form):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO Products
            (SKU, Name, Price, ProductCondition, Stock, Brand)
        VALUES
            (%s, %s, %s, %s, %s, %s)
        """,
        (
            form.sku.data,
            form.name.data,
            form.price.data,
            form.condition.data,
            form.stock.data,
            form.brand.data,
        ),
    )
    conn.commit()
    cursor.close()

def remove_product(form):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        """
        DELETE FROM Products
        WHERE ProductID = %s
        """,
        (form.product_id.data,),
    )
    conn.commit()
    cursor.close()

def get_db():
    if 'db' not in g:
        g.db =  mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE"),
        )
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()
