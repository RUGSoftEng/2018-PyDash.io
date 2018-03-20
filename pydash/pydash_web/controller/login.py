"""
Manages the logging in of a user into the application,
and rejecting visitors that enter improper sign-in information.
"""
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user
from werkzeug.urls import url_parse
import pydash_app.user

from pydash_web.forms import LoginForm


def login():
    if current_user.is_authenticated:
        return redirect(url_for("pydash_web.dashboard"))

    login_form = LoginForm()
    if not login_form.validate_on_submit():
        return __render_login_form(login_form)

    user = pydash_app.user.authenticate(login_form.username.data,
                                        login_form.password.data)
    if not user:
        flash("Wrong username or password!")
        return __render_login_form(login_form)

    login_user(user, remember=login_form.remember_me.data)
    flash("User {} successfully logged in!".format(user.name))
    return redirect(__next_page())


def __next_page():
    next = request.args.get('next')
    if not next or url_parse.netloc(next) != '':
        next = url_for("pydash_web.dashboard")
    return next


def __render_login_form(login_form):
    return render_template(
        "login.html", title="Sign In", login_form=login_form)
