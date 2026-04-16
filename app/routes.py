from flask import render_template, flash, redirect
from app import app
from app.forms import LoginForm, TransactionForm, TransactionItemForm

@app.route('/')
@app.route('/index')
@app.route('/employee', methods=['GET', 'POST'])
def employee():
    transaction_form = TransactionForm()
    item_form = TransactionItemForm()
    if transaction_form.validate_on_submit() and item_form.validate():
        transaction_type = transaction_form.transaction_type.data
        customer = transaction_form.customer.data
        employee = transaction_form.employee.data
        payment_method = transaction_form.payment_method.data
        product_id = item_form.product.product_id.data
        quantity = item_form.quantity.data
        flash('Transaction submitted')
        return redirect('/index')
    return render_template('employee.html', title='Employee',
                           transaction_form=transaction_form, item_form=item_form)

@app.route('/manager', methods=['GET', 'POST'])
def manager():
    return render_template('manager.html', title='Manager')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', title='Sign In', form=form)