import mysql.connector
from flask import render_template, flash, redirect, request, url_for
from app import app
from app.database import (
    get_db,
    fetch_employees,
    fetch_products,
    add_employee,
    update_employee_status,
    terminate_employee,
    add_product,
    remove_product
)
from app.forms import (
    TransactionForm,
    AddEmployeeForm,
    AddProductForm,
    RemoveProductForm,
    TerminateEmployeeForm,
    UpdateEmployeeStatusForm,
)

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
    terminate_form = TerminateEmployeeForm()

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

            if form_name == 'terminate_employee' and terminate_form.validate_on_submit():
                terminate_employee(terminate_form)
                flash('Employee terminated')
                return redirect(url_for('manager'))
        except mysql.connector.Error:
            flash('The database could not save your changes.')

    return render_template(
        'manager.html',
        title='Manager',
        employee_form=employee_form,
        status_form=status_form,
        terminate_form=terminate_form,
        employees=fetch_employees(),
    )

@app.route('/inventory', methods=['GET', 'POST'])
def inventory():
    form = AddProductForm()
    remove_form = RemoveProductForm()

    if request.method == 'POST':
        form_name = request.form.get('form_name')
        try:
            if form_name == 'add_product' and form.validate_on_submit():
                add_product(form)
                flash('Products added')
                return redirect(url_for('inventory'))

            if form_name == 'remove_product' and remove_form.validate_on_submit():
                remove_product(remove_form)
                flash('Product removed')
                return redirect(url_for('inventory'))
        except mysql.connector.Error:
            flash('The database could not save your changes.')
            return redirect(url_for('inventory'))

    return render_template(
        'products.html',
        title='Products',
        form=form,
        remove_form=remove_form,
        products=fetch_products(),
    )
