"""
Serves as a blueprint for the entire pydash_web package.
url_for() calls within this package should prepend 'pydash_web.' to their input argument.
  [e.g. url_for(login) becomes url_for(pydash_web.login) ]
route decorators in this package should also use this blueprint object instead of the flask application object.
"""

from flask import Blueprint

api = Blueprint('pydash_web.api', __name__, static_folder="../../pydash-front/build", static_url_path="")

import pydash_web.api_routes
