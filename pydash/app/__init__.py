from flask import Flask
from flask_login import LoginManager

from config import Config

from app.model.datastore import seed_datastore
from app.model.user import User

app = Flask(__name__)
app.config.from_object(Config)
login = LoginManager(app)
login.login_view = 'login'

@login.user_loader
def load_user(name):
    return User.find_user_by_name(name)

from app import routes

@app.cli.command('seed')
def seed_command():
    """Initializes our datastore with some preliminary values"""
    seed_datastore();

@app.shell_context_processor
def make_shell_context():
    return {'User': User}
