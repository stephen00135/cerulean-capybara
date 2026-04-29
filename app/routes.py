import mysql.connector
from flask import render_template, flash, redirect, request, url_for
from app import app
from app.database import get_db
from app.forms import (
    TransactionForm,
    AddEmployeeForm,
    AddProductForm,
    UpdateEmployeeStatusForm,
)

def fetch_employees():
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT id, first_name, last_name, phone, email, status, title, hourly_wage
            FROM employees
            ORDER BY last_name, first_name
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
            SELECT id, sku, name, price, `condition`, stock, brand
            FROM products
            ORDER BY name
            """
        )
        products = cursor.fetchall()
        cursor.close()
        return products
    except mysql.connector.Error:
        flash('Could not load inventory from the database.')
        return []

def add_employee(form):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO employees
            (first_name, last_name, phone, email, status, title, hourly_wage)
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
        UPDATE employees
        SET status = %s
        WHERE id = %s
        """,
        (form.status.data, form.employee_id.data),
    )
    conn.commit()
    cursor.close()

def add_product(form):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO products
            (sku, name, price, `condition`, stock, brand)
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

@app.route('/')
@app.route('/index')
@app.route('/employee', methods=['GET', 'POST'])
def employee():
    form = TransactionForm()
    if form.validate_on_submit():
        conn = get_db()
        cursor = conn.cursor()
        transaction_type = form.transaction_type.data
        customer = form.customer.data
        employee = form.employee.data
        payment_method = form.payment_method.data
        items = []
        for item in form.items:
            items.append({
                'product_id': item.product.product_id.data, # type: ignore
                'quantity': item.quantity.data
            })
        cursor.close()
        flash('Transaction submitted')
        return redirect('/index')
    return render_template('transaction.html', title='Transaction', form=form)

@app.route('/manager', methods=['GET', 'POST'])
def manager():
    employee_form = AddEmployeeForm()
    status_form = UpdateEmployeeStatusForm()

    if request.method == 'POST':
        form_name = request.form.get('form_name')
        try:
            if form_name == 'add_employee' and employee_form.validate_on_submit():
                add_employee(employee_form)
                flash('Employee added')
                return redirect(url_for('manager'))

            if form_name == 'update_employee_status' and status_form.validate_on_submit():
                update_employee_status(status_form)
                flash('Employee status updated')
                return redirect(url_for('manager'))
        except mysql.connector.Error:
            flash('The database could not save your changes.')

    return render_template(
        'manager.html',
        title='Manager',
        employee_form=employee_form,
        status_form=status_form,
        employees=fetch_employees(),
    )

@app.route('/inventory', methods=['GET', 'POST'])
def inventory():
    form = AddProductForm()
    if form.validate_on_submit():
        try:
            add_product(form)
        except mysql.connector.Error:
            flash('The database could not save your changes.')
            return redirect(url_for('inventory'))

        flash('Product added')
        return redirect(url_for('inventory'))

    return render_template(
        'inventory.html',
        title='Inventory',
        form=form,
        products=fetch_products(),
    )
