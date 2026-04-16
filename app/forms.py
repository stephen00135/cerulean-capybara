from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, BooleanField, FieldList,
                      SubmitField, SelectField, IntegerField, FormField)
from wtforms.validators import DataRequired, Optional, Length, NumberRange
from wtforms.form import Form

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class ProductForm(Form):
    product_id = IntegerField('Product ID', validators=[DataRequired()])

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
            ('trade', 'trade'),
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
