# finance/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, DateTimeField, SubmitField, DateField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Optional
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


class BillForm(FlaskForm):
    name = StringField('Bill Name', validators=[DataRequired()])
    amount = FloatField('Amount Due', validators=[DataRequired()])
    due_date = DateField('Due Date', validators=[DataRequired()], format='%Y-%m-%d')
    billing_period_start = DateField('Billing Period Start', validators=[Optional()], format='%Y-%m-%d')
    billing_period_end = DateField('Billing Period End', validators=[Optional()], format='%Y-%m-%d')
    bill_type = SelectField('Bill Type', choices=[
        ('credit_card', 'Credit Card'),
        ('medical', 'Medical'),
        ('utility', 'Utility'),
        ('insurance', 'Insurance'),
        ('subscription', 'Subscription'),
        ('other', 'Other')
    ])
    status = SelectField('Status', choices=[
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue')
    ])
    payment_date = DateField('Payment Date', validators=[Optional()], format='%Y-%m-%d')
    account = SelectField('Associated Account', validators=[DataRequired()], coerce=int)
    notes = TextAreaField('Notes', validators=[Optional()])
    submit = SubmitField('Save Bill')

class IncomeForm(FlaskForm):
    source = StringField('Source', validators=[DataRequired()])
    amount = FloatField('Amount', validators=[DataRequired()])
    date_received = DateField('Date Received', validators=[DataRequired()])
    income_type = SelectField('Income Type', choices=[
        ('salary', 'Salary'), 
        ('dividend', 'Dividend'), 
        ('interest', 'Interest'),
        ('freelance', 'Freelance'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    is_recurring = BooleanField('Is Recurring')
    recurrence_pattern = SelectField('Recurrence Pattern', choices=[
        ('', 'None'),
        ('weekly', 'Weekly'),
        ('bi-weekly', 'Bi-Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('annually', 'Annually')
    ])
    next_expected_date = DateField('Next Expected Date', validators=[], format='%Y-%m-%d')
    description = TextAreaField('Description')
    account_id = SelectField('Account', coerce=int, validators=[Optional()])
    submit = SubmitField('Save')