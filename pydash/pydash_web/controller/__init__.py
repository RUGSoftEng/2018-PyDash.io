"""
The controller contains one dispatching function per flask_webapp endpoint action.
"""

from .login import login
from .logout import logout

from .register_user import register_user
from .user_verification import verify_user
from .delete_user import delete_user
from .change_settings import change_settings
from .change_password import change_password

from .dashboards import dashboards
from .dashboard import dashboard
from .register_dashboard import register_dashboard
from .change_dashboard_settings import change_dashboard_settings
from .delete_dashboard import delete_dashboard
from .execution_times_boxplots import endpoint_execution_times_boxplots
from .visitor_heatmap import visitor_heatmap
from .execution_times_per_version import execution_times_per_version
