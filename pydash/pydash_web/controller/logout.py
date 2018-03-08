from flask import redirect, url_for
from flask_login import logout_user

def logout():
    logout_user()
    return redirect(url_for("login"))
