"""
The controller contains one dispatching function per flask_webapp endpoint action.
"""

from .login import login
from .logout import logout
from .dashboards import dashboards
from .dashboards import dashboard
from .register_user import register_user
from .delete_user import delete_user
from .register_dashboard import register_dashboard
