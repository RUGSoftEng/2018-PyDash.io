"""
This module handles the persistence of `Dashboard` entities:

It is an adapter of the actual persistence layer, to insulate the application
from datastore-specific details.

It handles a subset of the following tasks
(specifically, it only actually contains functions for the tasks the application needs in its current state!):
- Creating new entities of the specified type.
- Finding them based on certain attributes.
- Persisting updated versions of existing entities.
- Deleting entities from the persistence layer.
"""
import uuid
import BTrees.OOBTree
import transaction
from pydash_database import database_root, MultiIndexedPersistentCollection


if not hasattr(database_root(), 'dashboards'):
    print("CREATING DASHBOARDS OBJECT")
    transaction.begin()
    database_root().dashboards = MultiIndexedPersistentCollection({'id'})
    transaction.commit()


def find(dashboard_id):
    # Ensure that this is also callable with strings or integers:
    if not isinstance(dashboard_id, uuid.UUID):
        dashboard_id = uuid.UUID(dashboard_id)
    print(f"Starting to look for dashboard {dashboard_id}")

    try:
        res = database_root().dashboards['id', dashboard_id]
        print(f"FOUND DASHBOARD in find_dashboard: {res}")
        return res
    except Exception as e:
        print(f"EXCEPTION: {e}")
        raise


def all():
    return database_root().dashboards.values()


def add(dashboard):
    try:
        database_root().dashboards.add(dashboard)
        transaction.commit()
    except KeyError:
        transaction.abort()
        raise


def update(dashboard):
    # Update item itself:
    transaction.commit()

    # Update indexes for item:
    for attempt in transaction.manager.attempts():
        with attempt:
            database_root().dashboards.update_item(dashboard)

def clear_all():
    transaction.begin()
    database_root().dashboards = MultiIndexedPersistentCollection({'id'})
    transaction.commit()
