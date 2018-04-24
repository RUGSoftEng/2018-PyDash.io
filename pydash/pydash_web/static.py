from flask import Blueprint

static = Blueprint('pydash_web.static', __name__,
                   static_folder='../../pydash-front/build/static',
                   static_url_path='/static')

import pydash_web.static_routes