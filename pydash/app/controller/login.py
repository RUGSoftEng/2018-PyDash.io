from flask_login import current_user, login_user, logout_user, login_required

def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    login_form = LoginForm();
    if not login_form.validate_on_submit():
        return render_template("login.html", title="Sign In", login_form=login_form)

    maybe_user = datastore.load()['users'].get(login_form.username.data)
    if not maybe_user or not maybe_user.check_password(login_form.password.data):
        flash("Wrong username or password!")
        return render_template("login.html", title="Sign In", login_form=login_form)

    login_user(maybe_user, remember=login_form.remember_me.data)
    flash("User {} successfully attempted to login!".format(maybe_user.name))
    return redirect(next_page())

def next_page():
    next = request.args.get('next')
    if not next or url_parse.netloc(next) != '':
        next = url_for("dashboard")
    return next
