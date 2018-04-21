"""
Entrypoint of `pydash_web`

Initializes a Flask web application, and loads the relevant configuration settings.
"""

from flask import Flask
from flask_login import LoginManager
from flask_cors import CORS

from pydash_web.api import api as api_blueprint


from config import Config

import pydash_app
import pydash_app.user
import pydash_app.dashboard


flask_webapp = Flask(__name__)
flask_webapp.config.from_object(Config)

flask_webapp.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(flask_webapp, resources={r"/api/*": {"origins": "*"}}, allow_headers=['Content-Type'], supports_credentials=True) # Only keep this during development!

flask_webapp.register_blueprint(api_blueprint)

login_manager = LoginManager(flask_webapp)


@login_manager.user_loader
def load_user(user_id):
    print("Loading user {}".format(user_id))
    try:
        return pydash_app.user.find(user_id)
    except KeyError:
        # Returning None signals the LoginManager that the login is invalid.
        # Everything else is handled automatically.
        return None


@flask_webapp.cli.command('seed', with_appcontext=False)
def seed_command():
    """Initializes our datastore with some preliminary values"""
    pydash_app.user.user_repository.seed_users()
    pydash_app.dashboard.dashboard_repository.seed_dashboards()
