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
                ID,
                FirstName,
                LastName,
                Phone,
                Email,
                Status,
                Title,
                HourlyWage
            FROM Employee
            ORDER BY LastName, FirstName
            """
        )
        employees = cursor.fetchall()
        cursor.close()
        return employees
    except mysql.connector.Error as e:
        flash(f'Could not load employees from the database: {e.msg}')
        return []

def fetch_products():
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT
                ID,
                SKU,
                Name,
                Price,
                ProductCondition,
                Stock,
                Brand
            FROM Product
            ORDER BY Name
            """
        )
        products = cursor.fetchall()
        cursor.close()
        return products
    except mysql.connector.Error as e:
        flash(f'Could not load products from the database: {e.msg}')
        return []
    
def fetch_transactions():
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT
                st.ID,
                st.Type,
                m.FirstName,
                m.LastName,
                e.FirstName as EmployeeFirstName,
                e.LastName as EmployeeLastName,
                st.Date,
                st.Total,
                st.PayMethod
            FROM SalesTransaction st
            LEFT JOIN Member m ON st.MemberID = m.ID
            LEFT JOIN Employee e ON st.EmployeeID = e.ID
            ORDER BY st.Date DESC
            LIMIT 50
            """
        )
        transactions = cursor.fetchall()
        cursor.close()
        return transactions
    except mysql.connector.Error as e:
        flash(f'Could not load transactions from the database: {e.msg}')
        return []
    
def fetch_transaction_items(transaction_id):
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT
                ti.ID,
                p.SKU,
                p.Name,
                ti.Quantity,
                ti.Total
            FROM TransactionItem ti
            JOIN Product p ON ti.ProductID = p.ID
            WHERE ti.SalesTransactionID = %s
            """,
            (transaction_id,)
        )
        items = cursor.fetchall()
        cursor.close()
        return items
    except mysql.connector.Error as e:
        flash(f'Could not load transaction items: {e.msg}')
        return []    

def add_employee(form):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO Employee
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
        UPDATE Employee
        SET Status = %s
        WHERE ID = %s
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
        UPDATE Employee
        SET Status = %s
        WHERE ID = %s
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
        INSERT INTO Product
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
        DELETE FROM Product
        WHERE ID = %s
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
