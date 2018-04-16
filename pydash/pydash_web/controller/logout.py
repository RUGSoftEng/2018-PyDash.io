"""
Allows a user to sign out again after finishing using the application
"""
from flask import jsonify
from flask_login import current_user, logout_user
import pydash_app.impl.logger as pylog

#logger = pylog.Logger(__name__)


def logout():
    if not current_user.is_authenticated:
        result = {"message": "User was not logged in"}
        #logger.warning(f"Logout failed - {current_user} was not logged in")
        return jsonify(result), 401

    #logger.info(f"{current_user} logged out successfully")
    logout_user()

    result = {"message": "User successfully logged out"}
    return jsonify(result)
