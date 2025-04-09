# finance/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, DateTimeField, SubmitField, DateField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileRequired, FileAllowed
from datetime import date

class AccountForm(FlaskForm):
    name = StringField('Account Name', validators=[DataRequired()])
    account_type = SelectField('Account Type', 
                             choices=[('checking', 'Checking'),
                                    ('savings', 'Savings'),
                                    ('credit', 'Credit Card'),
                                    ('investment', 'Investment')],
                             validators=[DataRequired()])
    balance = FloatField('Initial Balance', validators=[DataRequired()])
    submit = SubmitField('Submit', name='submit')

class TransactionForm(FlaskForm):
    account = SelectField('Account', coerce=int, validators=[DataRequired()]) # Added account field
    date = DateField('Date', validators=[DataRequired()], default=date.today)
    description = StringField('Description', validators=[DataRequired()])
    amount = FloatField('Amount', validators=[DataRequired()])
    category = StringField('Category')  # Added category field
    transaction_type = StringField('Transaction Type') # Added transaction_type field
    submit = SubmitField('Add Transaction')

class TransactionImportForm(FlaskForm):
    file = FileField('CSV File', validators=[
        FileRequired(),
        FileAllowed(['csv'], 'CSV files only!')
    ])
    account = SelectField('Account', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Import Transactions')