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