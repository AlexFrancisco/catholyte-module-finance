# finance/routes.py
import os
from werkzeug.utils import secure_filename
from flask import render_template, redirect, url_for, flash, current_app, request, abort
from flask_login import login_required, current_user
from app.modules.finance import finance_bp
from app.modules.finance.forms import AccountForm, TransactionForm, TransactionImportForm
from app.modules.finance.models import Account, Transaction
from app.modules.finance.importers.oneaz import import_oneaz_transactions
from app import db
from app.modules.finance.utils import categorize_transaction  # Import categorize_transaction
from app.modules.finance.forms import AccountForm, TransactionForm, TransactionImportForm, BillForm
from app.modules.finance.models import Account, Transaction, Bill
from datetime import datetime
@finance_bp.route('/accounts', methods=['GET', 'POST'])
@login_required
def accounts():
    form = AccountForm()
    if request.method == 'POST' and 'submit' in request.form:
        try:
            account = Account(
                name=form.name.data,
                account_type=form.account_type.data,
                balance=form.balance.data,
                user_id=current_user.id
            )
            db.session.add(account)
            db.session.commit()
            flash('Account added successfully!', 'success')
            return redirect(url_for('finance.accounts'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding account: {str(e)}', 'danger')
    
    accounts = Account.query.filter_by(user_id=current_user.id).all()
    return render_template('accounts.html', form=form, accounts=accounts)

@finance_bp.route('/accounts/<int:account_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_account(account_id):
    account = Account.query.get_or_404(account_id)
    # Verify account belongs to current user
    if account.user_id != current_user.id:
        abort(403)
        
    form = AccountForm(obj=account)
    if request.method == 'POST' and 'submit' in request.form:
        try:
            account.name = form.name.data
            account.account_type = form.account_type.data
            account.balance = form.balance.data
            db.session.commit()
            flash('Account updated successfully!', 'success')
            return redirect(url_for('finance.accounts'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating account: {str(e)}', 'danger')
        
    return render_template('edit_account.html', form=form, account=account)

@finance_bp.route('/accounts/<int:account_id>/delete', methods=['POST'])
@login_required
def delete_account(account_id):
    account = Account.query.get_or_404(account_id)
    # Verify account belongs to current user
    if account.user_id != current_user.id:
        abort(403)
        
    db.session.delete(account)
    db.session.commit()
    flash('Account deleted successfully!', 'success')
    return redirect(url_for('finance.accounts'))

@finance_bp.route('/transactions', methods=['GET', 'POST'])
@login_required
def transactions():
    form = TransactionForm()
    form.account.choices = [(a.id, a.name) for a in Account.query.filter_by(user_id=current_user.id)]
    
    if form.validate_on_submit():
        transaction = Transaction(
            description=form.description.data,
            amount=form.amount.data,
            transaction_type=form.transaction_type.data,
            date=form.date.data,
            account_id=form.account.data,
            user_id=current_user.id
        )
        db.session.add(transaction)
        db.session.commit()
        flash('Transaction added successfully!', 'success')
        return redirect(url_for('finance.transactions'))
        
    transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.date.desc()).all()
    return render_template('transactions.html', form=form, transactions=transactions)

@finance_bp.route('/transactions/<int:transaction_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_transaction(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    # Verify transaction belongs to current user
    if transaction.user_id != current_user.id:
        abort(403)
        
    form = TransactionForm(obj=transaction)
    form.account.choices = [(a.id, a.name) for a in Account.query.filter_by(user_id=current_user.id)]
    
    if request.method == 'POST' and 'submit' in request.form:
        try:
            transaction.description = form.description.data
            transaction.amount = form.amount.data
            transaction.transaction_type = form.transaction_type.data
            transaction.date = form.date.data
            transaction.account_id = form.account.data
            db.session.commit()
            flash('Transaction updated successfully!', 'success')
            return redirect(url_for('finance.transactions'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating transaction: {str(e)}', 'danger')
    
    return render_template('edit_transaction.html', form=form, transaction=transaction)

@finance_bp.route('/transactions/<int:transaction_id>/delete', methods=['POST'])
@login_required
def delete_transaction(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    # Verify transaction belongs to current user
    if transaction.user_id != current_user.id:
        abort(403)
        
    try:
        db.session.delete(transaction)
        db.session.commit()
        flash('Transaction deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting transaction: {str(e)}', 'danger')
    
    return redirect(url_for('finance.transactions'))

@finance_bp.route('/import', methods=['GET', 'POST'])
@login_required
def import_transactions():
    form = TransactionImportForm()
    form.account.choices = [(a.id, a.name) for a in Account.query.filter_by(user_id=current_user.id)]
    
    if form.validate_on_submit():
        file = form.file.data
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            count = import_oneaz_transactions(filepath, form.account.data)
            flash(f'Successfully imported {count} transactions!', 'success')
        except Exception as e:
            flash(f'Error importing transactions: {str(e)}', 'danger')
        finally:
            os.remove(filepath)  # Clean up uploaded file
            
        return redirect(url_for('finance.transactions'))
        
    return render_template('import.html', form=form)

@finance_bp.route('/dashboard')
@login_required
def dashboard():
    accounts = Account.query.filter_by(user_id=current_user.id).all()
    transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.date.desc()).limit(5).all()
    
    # Add bills to dashboard
    upcoming_bills = Bill.query.filter_by(user_id=current_user.id, status='pending') \
                             .order_by(Bill.due_date).limit(5).all()
    
    return render_template('finance_dashboard.html', 
                          accounts=accounts, 
                          transactions=transactions,
                          upcoming_bills=upcoming_bills)

@finance_bp.route('/transactions/add', methods=['GET', 'POST'])
@login_required
def add_transaction():
    form = TransactionForm()
    form.account.choices = [(a.id, a.name) for a in Account.query.filter_by(user_id=current_user.id)]
    
    if form.validate_on_submit():
        transaction = Transaction(
            account_id=form.account.data, # Use form.account.data instead of form.account_id.data
            date=form.date.data,
            description=form.description.data,
            amount=form.amount.data,
            user_id=current_user.id
        )
        # Call categorize_transaction to get the category from the LLM
        transaction.category = categorize_transaction(form.description.data)
        db.session.add(transaction)
        db.session.commit()
        flash('Transaction added successfully!', 'success')
        return redirect(url_for('finance.transactions'))
        
    return render_template('add_transaction.html', form=form)
@finance_bp.route('/bills', methods=['GET', 'POST'])
@login_required
def bills():
    form = BillForm()
    form.account.choices = [(a.id, a.name) for a in Account.query.filter_by(user_id=current_user.id)]
    
    if request.method == 'POST' and 'submit' in request.form:
        try:
            bill = Bill(
                name=form.name.data,
                amount=form.amount.data,
                due_date=form.due_date.data,
                billing_period_start=form.billing_period_start.data,
                billing_period_end=form.billing_period_end.data,
                bill_type=form.bill_type.data,
                status=form.status.data,
                payment_date=form.payment_date.data,
                notes=form.notes.data,
                account_id=form.account.data,
                user_id=current_user.id
            )
            db.session.add(bill)
            db.session.commit()
            flash('Bill added successfully!', 'success')
            return redirect(url_for('finance.bills'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding bill: {str(e)}', 'danger')
    
    # Get bills with filter options
    status_filter = request.args.get('status', 'all')
    type_filter = request.args.get('type', 'all')
    
    query = Bill.query.filter_by(user_id=current_user.id)
    
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)
    if type_filter != 'all':
        query = query.filter_by(bill_type=type_filter)
        
    bills = query.order_by(Bill.due_date).all()
    
    return render_template('bills.html', form=form, bills=bills, 
                          status_filter=status_filter, type_filter=type_filter)

@finance_bp.route('/bills/<int:bill_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_bill(bill_id):
    bill = Bill.query.get_or_404(bill_id)
    # Verify bill belongs to current user
    if bill.user_id != current_user.id:
        abort(403)
        
    form = BillForm(obj=bill)
    form.account.choices = [(a.id, a.name) for a in Account.query.filter_by(user_id=current_user.id)]
    
    if request.method == 'POST' and 'submit' in request.form:
        try:
            bill.name = form.name.data
            bill.amount = form.amount.data
            bill.due_date = form.due_date.data
            bill.billing_period_start = form.billing_period_start.data
            bill.billing_period_end = form.billing_period_end.data
            bill.bill_type = form.bill_type.data
            bill.status = form.status.data
            bill.payment_date = form.payment_date.data
            bill.account_id = form.account.data
            bill.notes = form.notes.data
            
            db.session.commit()
            flash('Bill updated successfully!', 'success')
            return redirect(url_for('finance.bills'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating bill: {str(e)}', 'danger')
        
    return render_template('edit_bill.html', form=form, bill=bill)

@finance_bp.route('/bills/<int:bill_id>/delete', methods=['POST'])
@login_required
def delete_bill(bill_id):
    bill = Bill.query.get_or_404(bill_id)
    # Verify bill belongs to current user
    if bill.user_id != current_user.id:
        abort(403)
        
    try:
        db.session.delete(bill)
        db.session.commit()
        flash('Bill deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting bill: {str(e)}', 'danger')
    
    return redirect(url_for('finance.bills'))

@finance_bp.route('/bills/<int:bill_id>/mark-paid', methods=['POST'])
@login_required
def mark_bill_paid(bill_id):
    bill = Bill.query.get_or_404(bill_id)
    # Verify bill belongs to current user
    if bill.user_id != current_user.id:
        abort(403)
        
    try:
        bill.status = 'paid'
        bill.payment_date = datetime.now().date()
        db.session.commit()
        flash('Bill marked as paid!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating bill: {str(e)}', 'danger')
    
    return redirect(url_for('finance.bills'))