import csv
from datetime import datetime
from app import db
from app.modules.finance.models import Transaction, Account

def import_oneaz_transactions(file_path, account_id):
    """Import OneAZ CSV transaction history into the database."""
    
    account = Account.query.get(account_id)
    if not account:
        raise ValueError("Account not found")

    def parse_date(date_str):
        """Convert date string to datetime, handling 2-digit years"""
        try:
            # First try the full year format
            return datetime.strptime(date_str, '%m/%d/%Y')
        except ValueError:
            # If that fails, try 2-digit year format
            dt = datetime.strptime(date_str, '%m/%d/%y')
            # Adjust years to handle the 2000s properly
            if dt.year > datetime.now().year - 2000:
                dt = dt.replace(year=dt.year + 1900)
            else:
                dt = dt.replace(year=dt.year + 2000)
            return dt

    with open(file_path, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        transactions = []
        
        for row in csvreader:
            amount = float(row['Amount'].replace('$', '').replace(',', ''))
            transaction_type = 'income' if amount > 0 else 'expense'
            amount = abs(amount)
            
            try:
                transaction_date = parse_date(row['Date'])
            except ValueError as e:
                raise ValueError(f"Error parsing date '{row['Date']}': {str(e)}")
            
            transaction = Transaction(
                description=row['Description'].strip(),
                amount=amount,
                transaction_type=transaction_type,
                date=transaction_date,
                account_id=account_id,
                user_id=account.user_id
            )
            transactions.append(transaction)
    
        db.session.bulk_save_objects(transactions)
        db.session.commit()
        
        return len(transactions)