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


@api.route("/api/logout", methods=["POST"])
def logout():
    return controller.logout()


@api.route("/api/dashboards", methods=["GET"])
@login_required
def get_dashboards():
    return controller.dashboards()


@api.route("/api/dashboards/<dashboard_id>", methods=["GET"])
@login_required
def get_dashboard(dashboard_id):
    return controller.dashboard(dashboard_id)


@api.route("/api/user/register", methods=["POST"])
def register_user():
    return controller.register_user()
