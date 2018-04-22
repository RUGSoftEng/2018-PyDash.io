"""
Entrypoint of `pydash_web`

Initializes a Flask web application, and loads the relevant configuration settings.
"""

from flask import Flask
from flask_login import LoginManager
from flask_cors import CORS
from pydash_web.blueprint import bp as pydash_web_bp

from config import Config

import pydash_app
import pydash_app.user
import pydash_app.dashboard


flask_webapp = Flask(__name__, static_folder="../../pydash-front/build", static_url_path="")
flask_webapp.config.from_object(Config)
login_manager = LoginManager(flask_webapp)
flask_webapp.register_blueprint(pydash_web_bp)
flask_webapp.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(flask_webapp, resources={r"/api/*": {"origins": "*"}}, allow_headers=['Content-Type'], supports_credentials=True) # Only keep this during development!


import datetime
from pydash_app.fetching.dashboard_fetch import start_default_scheduler, _add_dashboard_to_fetch_from

start_default_scheduler()

for dashboard in pydash_app.dashboard.dashboard_repository.all():
    print(f'Creating periodic task for {dashboard}')
    _add_dashboard_to_fetch_from(dashboard=dashboard, interval=datetime.timedelta(seconds=5))


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
