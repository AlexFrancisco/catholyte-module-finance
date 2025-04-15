# finance/__init__.py
from flask import Blueprint, request
from app.core.services.image_storage import ImageStorage
from app.core.services.image_service import get_latest_image_url
finance_bp = Blueprint('finance', __name__, template_folder='templates')

@finance_bp.context_processor
def inject_default_images():
    """Make default images available in all world module templates."""
    return {
        'DEFAULT_FINANCE_HEADER': get_latest_image_url('finance',None,None,'header-default'),
        'DEFAULT_BILL_HEADER_LONG': get_latest_image_url('finance',None,None,'header-bill-long'),
        'DEFAULT_BILL_HEADER_SHORT': get_latest_image_url('finance',None,None,'header-bill-short')
    }

@finance_bp.context_processor
def inject_template_vars():
    """Make default images and breadcrumbs available in all finance module templates."""
    # Define breadcrumb mappings based on routes
    breadcrumbs = {
        'finance.dashboard': [('Dashboard', None)],
        'finance.accounts': [('Dashboard', 'finance.dashboard'), ('Accounts', None)],
        'finance.edit_account': [('Dashboard', 'finance.dashboard'), ('Accounts', 'finance.accounts'), ('Edit Account', None)],
        'finance.transactions': [('Dashboard', 'finance.dashboard'), ('Transactions', None)],
        'finance.edit_transaction': [('Dashboard', 'finance.dashboard'), ('Transactions', 'finance.transactions'), ('Edit Transaction', None)],
        'finance.add_transaction': [('Dashboard', 'finance.dashboard'), ('Transactions', 'finance.transactions'), ('Add Transaction', None)],
        'finance.bills': [('Dashboard', 'finance.dashboard'), ('Bills & Invoices', None)],
        'finance.edit_bill': [('Dashboard', 'finance.dashboard'), ('Bills & Invoices', 'finance.bills'), ('Edit Bill', None)],
        'finance.import_transactions': [('Dashboard', 'finance.dashboard'), ('Import Transactions', None)],
    }
    
    # Get current endpoint
    current_endpoint = request.endpoint
    current_breadcrumbs = []
    
    # Add breadcrumbs for current route
    if current_endpoint in breadcrumbs:
        current_breadcrumbs = breadcrumbs[current_endpoint]
    
    return {
        # Default images
        'DEFAULT_FINANCE_HEADER': get_latest_image_url('finance', None, None, 'header-default'),
        'DEFAULT_BILL_HEADER_LONG': get_latest_image_url('finance', None, None, 'header-bill-long'),
        'DEFAULT_BILL_HEADER_SHORT': get_latest_image_url('finance', None, None, 'header-bill-short'),
        
        # Breadcrumb data
        'breadcrumbs': current_breadcrumbs
    }


from app.modules.finance import routes

def init_app(app):
    app.register_blueprint(finance_bp)