from flask import render_template
from app import app
from app.forms import LoginForm

@app.route("/index")
def index():
    user = {'username': 'Qqwy'}
    return render_template('index.html', title='Home', user=user)


@app.route("/")
@app.route("/login")
def login():
    login_form = LoginForm();
    return render_template("login.html", title="Sign In", login_form=login_form)
