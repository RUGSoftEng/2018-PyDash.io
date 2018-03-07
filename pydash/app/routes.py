from flask import render_template, flash, redirect
from app import app
from app.forms import LoginForm

@app.route("/index")
@app.route("/dashboard")
def index():
    return render_template('index.html', title='Home')


@app.route("/")
@app.route("/login", methods=["GET", "POST"])
def login_post():
    login_form = LoginForm();
    if login_form.validate_on_submit():
        flash("User attempted to login: {}".format(login_form.username.data))
        return redirect("/dashboard")
    else:
        return render_template("login.html", title="Sign In", login_form=login_form)
