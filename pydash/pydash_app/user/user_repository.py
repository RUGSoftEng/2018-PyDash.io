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
import uuid
import BTrees.OOBTree
import transaction
from ..impl.database import database_root, MultiIndexedPersistentCollection

from .user import User


if not hasattr(database_root, 'users'):
    database_root.users = MultiIndexedPersistentCollection({'id', 'name'})


def find(user_id):
    user_id = uuid.UUID(
        user_id)  # Ensure that also callable with strings or integers.
    return database_root.users['id', user_id]


def find_by_name(name):
    """
    Returns a single User-entity with the given `name`, or None if it could not be found.

    name -- Name of the user we hope to find.
    """
    return database_root.users.get('name', name, default=None)


def all():
    return database_root.users.values()


def add(user):
    try:
        database_root.users.add(user)
        transaction.commit()
    except KeyError:
        transaction.abort()
        raise


def update(user):
    try:
        database_root.users.update_item(user)
        transaction.commit()
    except KeyError:
        transaction.abort()
        raise


def seed_users():
    """
    Stores some preliminary debug users in the datastore,
    to be used during development.
    """

    # Clear current DB.
    database_root.users = MultiIndexedPersistentCollection({'id', 'name'})

    # Fill in users.
    _development_users = [
        User(name="Alberto", password="alberto"),
        User(name="Arjan", password="arjan"),
        User(name="JeroenO", password="jeroeno"),
        User(name="JeroenL", password="jeroenl"),
        User(name="Koen", password="koen"),
        User(name="Lars", password="lars"),
        User(name="Patrick", password="patrick"),
        User(name="Tom", password="tom"),
        User(name="W-M", password="topsecret")
    ]
    for user in _development_users:
        print("Adding user {}".format(user))
        add(user)
    print("Seeding of users is done!")
