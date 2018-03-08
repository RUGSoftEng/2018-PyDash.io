from flask import Flask
from flask_login import LoginManager

from config import Config

import pydash_app

# from pydash_app.datastore import seed_datastore
# from pydash_app.user import User

flask_webapp = Flask(__name__)
flask_webapp.config.from_object(Config)
login_manager = LoginManager(flask_webapp)
login_manager.login_view = 'login'

from pydash_web import routes  # Needs to be below flask_webapp instantiation


@login_manager.user_loader
def load_user(name):
    print("Loading user {}".format(name))
    return pydash_app.User.find_user_by_name(name)


@flask_webapp.cli.command('seed')
def seed_command():
    """Initializes our datastore with some preliminary values"""
    pydash_app.datastore.seed_datastore()


@flask_webapp.shell_context_processor
def make_shell_context():
    return {'User': pydash_app.User}
