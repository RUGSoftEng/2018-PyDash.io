"""
The controller contains one dispatching function per flask_webapp endpoint action.
"""

from .login import login
from .meta_dashboard import meta_dashboard
from .logout import logout
from .dashboards import get_dashboards
from .dashboards import get_dashboard
