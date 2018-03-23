"""
The controller contains one dispatching function per flask_webapp endpoint action.
"""

from .login import login
from .logout import logout
from .dashboards import dashboards
from .dashboards import dashboard
