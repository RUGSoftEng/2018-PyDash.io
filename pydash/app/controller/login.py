from flask_login import current_user, login_user, logout_user, login_required
from app.model.user import User

def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    login_form = LoginForm();
    if not login_form.validate_on_submit():
        return render_login_form(login_form)

    user = User.authenticate_user(login_form.name.data, login_form.password.data)
    if not user:
        flash("Wrong username or password!")
        return render_login_form(login_form)

    login_user(user, remember=login_form.remember_me.data)
    flash("User {} successfully attempted to login!".format(maybe_user.name))
    return redirect(next_page())

def next_page():
    next = request.args.get('next')
    if not next or url_parse.netloc(next) != '':
        next = url_for("dashboard")
    return next

def render_login_form(login_form):
        return render_template("login.html", title="Sign In", login_form=login_form)
