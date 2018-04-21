"""
Contains the different routes (web endpoints) that the pydash_web flask application can respond to.

The actual implementation of each of the routes' dispatching logic is handled by the respective 'controller' function.
"""

from flask_login import login_required
from flask_cors import cross_origin

from pydash_web.blueprint import bp
import pydash_web.controller as controller


@bp.route("/api/login", methods=["POST"])
def login():
    return controller.login()


@bp.route("/api/logout", methods=["POST"])
def logout():
    return controller.logout()


@bp.route("/api/dashboards", methods=["GET"])
@login_required
def get_dashboards():
    return controller.dashboards()


@bp.route("/api/dashboards/<dashboard_id>", methods=["GET"])
@login_required
def get_dashboard(dashboard_id):
    return controller.dashboard(dashboard_id)


# NOTE: Passing the plaintext password around like this would be very silly and a potential severe security risk.
#       Investigate on how to do this differently.
@bp.route("/api/register_user", methods=["POST"])
def register_user():
    return controller.register_user()


@bp.route("/", defaults={'path': ''})
@bp.route("/<path:path>")
def serve_react(path):
    return bp.send_static_file("index.html")
