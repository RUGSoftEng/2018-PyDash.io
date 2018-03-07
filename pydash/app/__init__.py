from flask import Flask
from config import Config

from app.model.datastore import seed_datastore
from app.model.user import User

app = Flask(__name__)
app.config.from_object(Config)

from app import routes

@app.cli.command('seed')
def seed_command():
    """Initializes our datastore with some preliminary values"""
    seed_datastore();

@app.shell_context_processor
def make_shell_context():
    return {'User': User}
