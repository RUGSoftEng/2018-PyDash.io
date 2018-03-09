"""
The controller contains one dispatching function per flask_webapp endpoint action.
"""

from .login import login
from .dashboard import dashboard
from .logout import logout
