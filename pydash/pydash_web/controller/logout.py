"""
Allows a user to sign out again after finishing using the application
"""
from flask import jsonify
from flask_login import current_user, logout_user


def logout():
    if not current_user.is_authenticated:
        result = {"message": "User was not logged in"}
        return jsonify(result), 401

    logout_user()

    result = {"message": "User successfully logged out"}
    return jsonify(result)
