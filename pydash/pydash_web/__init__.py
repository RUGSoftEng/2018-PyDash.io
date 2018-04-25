"""
Entrypoint of `pydash_web`

Initializes a Flask web application, and loads the relevant configuration settings.
"""
import os

from flask import Flask
from flask_login import LoginManager
from flask_cors import CORS

from pydash_web.api import api as api_blueprint
from pydash_web.static import static as static_blueprint

from config import Config

import pydash_app
import pydash_app.user


flask_webapp = Flask(__name__)
flask_webapp.config.from_object(Config)

flask_webapp.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(flask_webapp, resources={r"/api/*": {"origins": "*"}}, allow_headers=['Content-Type'], supports_credentials=True) # Only keep this line during development!

flask_webapp.register_blueprint(api_blueprint)
flask_webapp.register_blueprint(static_blueprint)

pydash_app.schedule_periodic_tasks()

# Don't autostart scheduler in the testing environment.
print(os.environ)
if 'TESTING' not in os.environ:
    pydash_app.start_task_scheduler()

login_manager = LoginManager(flask_webapp)
@login_manager.user_loader
def load_user(user_id):
    print("Loading user {}".format(user_id))
    return pydash_app.user.maybe_find_user(user_id)


@flask_webapp.cli.command('seed', with_appcontext=False)
def seed_command():
    """Initializes our datastore with some preliminary values"""
    pydash_app.seed_datastructures()
