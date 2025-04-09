# finance/__init__.py
from flask import Blueprint

finance_bp = Blueprint('finance', __name__, template_folder='templates')

from app.modules.finance import routes