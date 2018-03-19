"""
This module is the public interface (available to the web-application pydash_web)
for interacting with Users.
"""
from .user import User
import pydash_app.user.user_repository

def find(user_id):
    """
    Reutnrs a single User-entity with the given UUID or None if it could not be found.

    user_id- UUID of the user we hope to find."""
    return user_repository.find(user_id)

def find_by_name(name):
    """
    Returns a single User-entity with the given `name`, or None if it could not be found.

    name -- Name of the user we hope to find.
    """
    return user_repository.find_by_name(name)


def authenticate(name, password):
    """
    Attempts to authenticate the user with name `name`
    and password `password`.

    If authentication fails (unknown user or incorrect password), returns None.
    Otherwise, returns the user object.
    """
    maybe_user = find_by_name(name)
    if maybe_user == None or maybe_user.check_password(password) == False:
        return None
    return maybe_user
