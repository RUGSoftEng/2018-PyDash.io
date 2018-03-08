from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user, login_required

from app.forms import LoginForm
import app.model.datastore as datastore
from app import app

@app.route("/index")
def index():
    return render_template('index.html', title='Home')

@app.route("/")
@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    login_form = LoginForm();
    if login_form.validate_on_submit():
        # flash("User attempted to login: {}".format(login_form.username.data))
        maybe_user = datastore.load()['users'].get(login_form.username.data)
        if maybe_user and maybe_user.check_password(login_form.password.data):
            login_user(maybe_user, remember=login_form.remember_me.data)
            flash("User {} successfully attempted to login!".format(maybe_user.name))
            # TODO read next page parameter.
            return redirect(url_for("dashboard"))
        else:
            flash("Wrong username or password!")
            return render_template("login.html", title="Sign In", login_form=login_form)
    else:
        return render_template("login.html", title="Sign In", login_form=login_form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template('dashboard.html');
