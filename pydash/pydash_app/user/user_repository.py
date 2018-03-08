"""
This module handles the persistence of `User` entities:

It is an adapter of the actual persistence layer, to insulate the application
from datastore-specific details.

It handles a subset of the following tasks
(specifically, it only actually contains functions for the tasks the application needs in its current state!):
- Creating new entities of the specified type
- Finding them based on certain attributes
- Persisting updated versions of existing entities.
- Deleting entities from the persistence layer.
"""


from .user import User


def find_by_name(name):
    """
    Returns a single User-entity with the given `name`, or None if it could not be found.

    name -- Name of the user we hope to find.
    """
    return _hard_coded_users_dict().get(name)


def _hard_coded_users_dict():
    """
    Sneakily our user datastore is currently a hard-coded list of users!
    """
    return {"Qqwy": User(name="Qqwy", password="topsecret")}
