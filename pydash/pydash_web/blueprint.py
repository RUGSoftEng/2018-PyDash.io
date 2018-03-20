from flask import Blueprint

bp = Blueprint('pydash_web', __name__)

from pydash_web import routes