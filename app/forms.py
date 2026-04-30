from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, BooleanField, FieldList,
                      SubmitField, SelectField, IntegerField, FormField, DecimalField,
                      HiddenField)
from wtforms.validators import DataRequired, Optional, Length, NumberRange
from wtforms.form import Form

class ProductForm(Form):
    sku = StringField('SKU', validators=[DataRequired(), Length(max=50)])

class TransactionItemForm(Form):
    product = FormField(ProductForm)
    quantity = IntegerField(
        'Quantity',
        validators=[DataRequired(), NumberRange(min=1, max=50)]
    )

class TransactionForm(FlaskForm):
    transaction_type = SelectField(
        'Type',
        choices=[
            ('sale', 'sale'),
            ('return', 'return'),
        ],
        validators=[DataRequired()]
    )
    customer = StringField('Customer Email', validators=[Optional(), Length(max=100)])
    employee = StringField('Employee Email', validators=[Optional(), Length(max=100)])

    payment_method = SelectField(
        'Payment Method',
        choices=[
            ('credit', 'credit'),
            ('debit', 'debit'),
            ('cash', 'cash')
        ],
        validators=[DataRequired()]
    )

    items = FieldList(FormField(TransactionItemForm), min_entries=1)

    submit = SubmitField('Submit')

class AddProductForm(FlaskForm):
    sku = StringField('SKU', validators=[DataRequired(), Length(max=50)])
    name = StringField('Product Name', validators=[DataRequired(), Length(max=100)])
    price = DecimalField(
        'Price',
        validators=[DataRequired(), NumberRange(min=0)],
        places=2
    )
    condition = SelectField(
        'Condition',
        choices=[
            ('new', 'new'),
            ('used', 'used')
        ],
        validators=[DataRequired()]
    )
    stock = IntegerField('Stock', validators=[DataRequired(), NumberRange(min=0)])
    brand = StringField('Brand', validators=[Optional(), Length(max=100)])
    submit = SubmitField('Add Product')

class AddEmployeeForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=20)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=20)])
    phone = StringField('Phone', validators=[Optional(), Length(max=20)])
    email = StringField('Email', validators=[DataRequired(), Length(max=100)])
    status = SelectField(
        'Status',
        choices=[
            ('active', 'active'),
            ('terminated', 'terminated')
        ],
        validators=[DataRequired()]
    )
    title = StringField('Title', validators=[Optional(), Length(max=50)])
    hourly_wage = DecimalField(
        'Hourly Wage',
        validators=[Optional(), NumberRange(min=0)],
        places=2
    )
    submit = SubmitField('Add Employee')

class UpdateEmployeeStatusForm(FlaskForm):
    employee_id = HiddenField('Employee ID', validators=[DataRequired()])
    status = SelectField(
        'Status',
        choices=[
            ('active', 'active'),
            ('terminated', 'terminated')
        ],
        validators=[DataRequired()]
    )
    submit = SubmitField('Update')

class TerminateEmployeeForm(FlaskForm):
    employee_id = HiddenField('Employee ID', validators=[DataRequired()])
    submit = SubmitField('Terminate')

class RemoveProductForm(FlaskForm):
    product_id = HiddenField('Product ID', validators=[DataRequired()])
    submit = SubmitField('Remove')
