from flask import Flask
from flask_login import LoginManager

from config import Config

from app.model.datastore import seed_datastore
from app.model.user import User

flask_app = Flask(__name__)
flask_app.config.from_object(Config)
login = LoginManager(flask_app)
login.login_view = 'login'

from app import routes  # Needs to be below flask_app instantiation


@login.user_loader
def load_user(name):
    print("Loading user {}".format(name))
    return User.find_user_by_name(name)


@flask_app.cli.command('seed')
def seed_command():
    """Initializes our datastore with some preliminary values"""
    seed_datastore()


@flask_app.shell_context_processor
def make_shell_context():
    return {'User': User}
