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
from pydash_database import database_root, MultiIndexedPersistentCollection
from multi_indexed_collection import DuplicateIndexError

from .user import User


if not hasattr(database_root(), 'users'):
    transaction.begin()
    database_root().users = MultiIndexedPersistentCollection({'id', 'name'})
    transaction.commit()


def find(user_id):
    # Ensure that also callable with strings or integers:
    if not isinstance(user_id, uuid.UUID):
        user_id = uuid.UUID(user_id)

    return database_root().users['id', user_id]


def find_by_name(name):
    """
    Returns a single User-entity with the given `name`, or None if it could not be found.

    name -- Name of the user we hope to find.
    """
    return database_root().users.get('name', name, default=None)


def all():
    """
    Returns a (lazy) collection of all users (in no guaranteed order).

    >>> list(all())
    []
    >>> gandalf = User("Gandalf", "pass")
    >>> dumbledore = User("Dumbledore", "secret")
    >>> add(gandalf)
    >>> add(dumbledore)
    >>> sorted([user.name for user in all()])
    ['Dumbledore', 'Gandalf']
    >>> clear_all()
    >>> sorted([user.name for user in all()])
    []
    """
    return database_root().users.values()


def add(user):
    try:
        transaction.begin()
        database_root().users.add(user)
        transaction.commit()
    except (KeyError, DuplicateIndexError):
        transaction.abort()
        raise


def update(user):
    """
    Changes the user's information


    >>> gandalf = User("GandalfTheGrey", "pass")
    >>> add(gandalf)
    >>> gandalf.name = "GandalfTheWhite"
    >>> update(gandalf)
    >>> find_by_name("GandalfTheGrey") == gandalf
    False
    >>> find_by_name("GandalfTheWhite") == gandalf
    True

    """
    transaction.commit()
    for attempt in transaction.manager.attempts():
        with attempt:
            database_root().users.update_item(user)
    transaction.begin()

def clear_all():
    """
    Flushes the database.
    """
    transaction.begin()
    database_root().users = MultiIndexedPersistentCollection({'id', 'name'})
    transaction.commit()
