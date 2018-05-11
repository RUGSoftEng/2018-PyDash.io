"""
Manages changing of the user's password.
"""

from flask import jsonify
from flask_login import current_user
from flask_restplus.reqparse import RequestParser


def change_password():
    pass


def _parse_args():
    parser = RequestParser()
    parser.add_argument('current_password')
    parser.add_argument('new_password')
    return parser.parse_args()