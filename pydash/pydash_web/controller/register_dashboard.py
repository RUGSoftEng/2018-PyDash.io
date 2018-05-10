from flask import jsonify
from flask_login import current_user
from pydash_app.dashboard.dashboard import DashboardState
from flask_restplus.reqparse import RequestParser

import pydash_app.dashboard
import pydash_logger


def register_dashboard():
    pass


def _parse_arguments():
    parser = RequestParser()
    parser.add_argument('username')
    parser.add_argument('password')
    return parser.parse_args()