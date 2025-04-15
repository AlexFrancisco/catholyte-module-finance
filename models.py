# finance/models.py
from app import db
from flask_login import current_user
from datetime import datetime

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    account_type = db.Column(db.String(50), nullable=False)
    balance = db.Column(db.Float, nullable=False, default=0.0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    transactions = db.relationship('Transaction', back_populates='account')

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(255), nullable=True)  # Added category field
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Define user_id as ForeignKey
    transaction_type = db.Column(db.String(50), nullable=True) # Added transaction_type field
    
    def __repr__(self):
        return f'<Transaction {self.description}>'
    
    account = db.relationship('Account', back_populates='transactions')

class Bill(db.Model):
    __tablename__ = 'bills'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    billing_period_start = db.Column(db.Date, nullable=True)
    billing_period_end = db.Column(db.Date, nullable=True)
    bill_type = db.Column(db.String(50), nullable=False)  # Credit card, medical, utility, etc.
    status = db.Column(db.String(20), default='pending')  # pending, paid, overdue
    payment_date = db.Column(db.Date, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    
    # Foreign keys
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relationships
    account = db.relationship('Account', backref=db.backref('bills', lazy=True))
    user = db.relationship('User', backref=db.backref('bills', lazy=True))
    
    def __repr__(self):
        return f"<Bill {self.name} - ${self.amount} due on {self.due_date}>"
    
class Income(db.Model):
    __tablename__ = 'income'
    
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(100), nullable=False)  # Employer name, investment source, etc.
    amount = db.Column(db.Float, nullable=False)
    date_received = db.Column(db.Date, nullable=False)
    income_type = db.Column(db.String(50), nullable=False)  # Salary, dividend, interest, freelance, etc.
    is_recurring = db.Column(db.Boolean, default=False)  # Whether this is a regular income source
    recurrence_pattern = db.Column(db.String(50), nullable=True)  # weekly, bi-weekly, monthly if recurring
    next_expected_date = db.Column(db.Date, nullable=True)  # When next income is expected if recurring
    description = db.Column(db.Text, nullable=True)  # Additional details
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    
    # Relationships
    user = db.relationship('User', backref=db.backref('incomes', lazy=True))
    account = db.relationship('Account', backref=db.backref('incomes', lazy=True))
    
    def __repr__(self):
        return f"<Income {self.source} - ${self.amount} received on {self.date_received}>"