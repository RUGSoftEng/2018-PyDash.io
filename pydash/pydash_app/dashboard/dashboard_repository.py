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
from ..impl.database import database_root, MultiIndexedPersistentCollection

from .dashboard import Dashboard
from pydash_app.user import user_repository

if not hasattr(database_root, 'dashboards'):
    database_root.dashboards = MultiIndexedPersistentCollection({'id'})


def find(dashboard_id):
    # Ensure that this is also callable with strings or integers:
    dashboard_id = uuid.UUID(dashboard_id)

    return database_root.dashboards['id', dashboard_id]


def all():
    return database_root.dashboards.values()


def add(dashboard):
    try:
        database_root.dashboards.add(dashboard)
        transaction.commit()
    except KeyError:
        transaction.abort()
        raise


def update(dashboard):
    try:
        database_root.dashboards.update_item(dashboard)
        transaction.commit()
    except KeyError:
        transaction.abort()
        raise


def seed_dashboards():
    """
    Stores some preliminary debug dashboards in the datastore,
    to be used during development.
    """

    # Clear current Dashboards-DB.
    database_root.dashboards = MultiIndexedPersistentCollection({'id'})
    _dev_dashboard_urls = ['http://pydash.io/', 'http://pystach.io/']

    # Fill in dashboards.
    for user in user_repository.all():
        for url in _dev_dashboard_urls:
            dashboard = Dashboard(url, user.get_id())
            print(f'Adding dashboard {dashboard}')
            add(dashboard)

    print('Seeding of dashboards is done!')
