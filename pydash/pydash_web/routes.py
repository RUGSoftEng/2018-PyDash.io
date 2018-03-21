"""
Contains the different routes (web endpoints) that the pydash_web flask application can respond to.

The actual implementation of each of the routes' dispatching logic is handled by the respective 'controller' function.
"""

from flask_login import login_required

from pydash_web.blueprint import bp
import pydash_web.controller as controller


@bp.route("/api/login", methods=["POST"])
def login():
    return controller.login()


@bp.route("/api/logout", methods=["POST"])
def logout():
    return controller.logout()


@bp.route("/dashboard")
@login_required
def dashboard():
    return controller.dashboard()
