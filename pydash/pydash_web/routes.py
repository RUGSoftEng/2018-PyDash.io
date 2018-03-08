"""
Contains the different routes (web endpoints) that the pydash_web flask application can respond to.

The actual implementation of each of the routes' dispatching logic is handled by the respective 'controller' function.
"""

from flask import render_template
from flask_login import current_user, login_user, logout_user, login_required

from pydash_web import flask_webapp
import pydash_web.controller as controller


@flask_webapp.route("/")
@flask_webapp.route("/login", methods=["GET", "POST"])
def login():
    return controller.login()


@flask_webapp.route("/logout")
def logout():
    return controller.logout()


@flask_webapp.route("/dashboard")
@login_required
def dashboard():
    return controller.dashboard()
