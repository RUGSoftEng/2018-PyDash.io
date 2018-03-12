"""
Entrypoint of `pydash_web`

Initializes a Flask web application, and loads the relevant configuration settings.
"""

from flask import Flask
from flask_login import LoginManager

from config import Config

import pydash_app

flask_webapp = Flask(__name__, static_folder="../../pydash-front/build", static_url_path="")
flask_webapp.config.from_object(Config)
login_manager = LoginManager(flask_webapp)
login_manager.login_view = 'login'


from pydash_web import routes  # Needs to be below flask_webapp instantiation to prevent circular dependency


@login_manager.user_loader
def load_user(name):
    print("Loading user {}".format(name))
    return pydash_app.user.find_by_name(name)


@flask_webapp.cli.command('seed')
def seed_command():
    """Initializes our datastore with some preliminary values"""
    pydash_app.datastore.seed_datastore()
