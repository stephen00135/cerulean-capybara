from flask import render_template, flash, redirect
from app import app
from app.database import get_db
from app.forms import TransactionForm, TransactionItemForm

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
    return render_template('employee.html', title='Employee', form=form)

@app.route('/manager', methods=['GET', 'POST'])
def manager():
    return render_template('manager.html', title='Manager')
