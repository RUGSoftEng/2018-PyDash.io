"""
Contains the different routes (web endpoints) that the pydash_web flask application can respond to.

The actual implementation of each of the routes' dispatching logic is handled by the respective 'controller' function.
"""

from flask_login import login_required

from pydash_web.api import api
import pydash_web.controller as controller


@api.route("/api/login", methods=["POST"])
def login():
    return controller.login()


# No @login_required, because this is handled internally.
@api.route("/api/logout", methods=["POST"])
def logout():
    return controller.logout()


@api.route("/api/user/register", methods=["POST"])
def register_user():
    return controller.register_user()


@api.route("/api/user/verify", methods=["POST"])
def verify_user():
    return controller.verify_user()


@api.route("/api/user/delete", methods=["POST"])
@login_required
def delete_user():
    return controller.delete_user()


@api.route("/api/user/change_settings", methods=["POST"])
@login_required
def change_settings():
    return controller.change_settings()


@api.route("/api/user/change_password", methods=["POST"])
@login_required
def change_password():
    return controller.change_password()


@api.route("/api/dashboards/<dashboard_id>/change_settings", methods=["POST"])
@login_required
def change_dashboard_settings(dashboard_id):
    return controller.change_dashboard_settings(dashboard_id)


@api.route("/api/dashboards", methods=["GET"])
@login_required
def get_dashboards():
    return controller.dashboards()


@api.route("/api/dashboards/<dashboard_id>", methods=["GET"])
@login_required
def get_dashboard(dashboard_id):
    return controller.dashboard(dashboard_id)


@api.route("/api/dashboards/register", methods=["POST"])
@login_required
def register_dashboard():
    return controller.register_dashboard()


@api.route("/api/dashboards/<dashboard_id>/delete", methods=["POST"])
@login_required
def delete_dashboard(dashboard_id):
    return controller.delete_dashboard(dashboard_id)


@api.route("/api/dashboards/<dashboard_id>/endpoint_boxplots", methods=["GET"])
@login_required
def get_endpoint_boxplots(dashboard_id):
    return controller.endpoint_boxplots(dashboard_id)


@api.route("/api/dashboards/<dashboard_id>/visitor_heatmap", methods=["GET"])
@login_required
def get_visitor_heatmap(dashboard_id):
    return controller.visitor_heatmap(dashboard_id)


@api.route("/api/dashboards/<dashboard_id>/unique_visitor_heatmap", methods=["GET"])
@login_required
def get_unique_visitor_heatmap(dashboard_id):
    return controller.visitor_heatmap(dashboard_id, 'unique_visitors')


@api.route("/api/dashboards/<dashboard_id>/execution_times_per_version", methods=["GET"])
@login_required
def get_response_time_per_version_dashboard(dashboard_id):
    return controller.execution_times_per_version(dashboard_id=dashboard_id)


@api.route("/api/dashboards/<dashboard_id>/endpoints/<endpoint_name>/execution_times_per_version", methods=["GET"])
@login_required
def get_response_time_per_version_endpoint(dashboard_id, endpoint_name):
    return controller.execution_times_per_version(dashboard_id=dashboard_id, endpoint_name=endpoint_name)
