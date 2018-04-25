"""
This module is the public interface (available to the web-application pydash_web)
for interacting with Users.
"""
from .user import User
import pydash_app.user.user_repository


def add_to_repository(user):
    """
    Adds the given User-entity to the user_repository. Raises a KeyError if the user is already in the repository.
    :param user: The User-entity in question.
    """
    try:
        user_repository.add(user)
    except KeyError:
        raise


def remove_from_repository(user):
    """
    Removes the given User-entity from the user_repository. Raises a KeyError if the user is not in the repository.
    :param user: The user-entity in question.
    """
    try:
        user_repository.delete(user)
    except KeyError:
        raise


def find(user_id):
    """
    Returns a single User-entity with the given UUID or None if it could not be found.

    user_id- UUID of the user we hope to find."""
    return user_repository.find(user_id)


def maybe_find_user(user_id):
    """
    Returns the User entity, or `None` if it does not exist.
    """
    try:
        return pydash_app.user.find(user_id)
    except KeyError:
        return None


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
    if maybe_user is None or not maybe_user.check_password(password):
        return None
    return maybe_user
