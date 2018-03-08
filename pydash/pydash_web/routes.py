from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required

import pydash_app.datastore as datastore
from pydash_web import flask_webapp
import pydash_web.controller.login

@flask_webapp.route("/index")
def index():
    return render_template('index.html', title='Home')

@flask_webapp.route("/")
@flask_webapp.route("/login", methods=["GET", "POST"])
def login():
    return pydash_web.controller.login.login()


@flask_webapp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))

@flask_webapp.route("/dashboard")
@login_required
def dashboard():
    return render_template('dashboard.html');
