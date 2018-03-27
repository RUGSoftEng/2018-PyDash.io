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


if not hasattr(database_root, 'dashboards'):
    database_root.dashboards = MultiIndexedPersistentCollection({'id', 'url'})


def find(dashboard_id):
    # Ensure that this is also callable with strings or integers:
    dashboard_id = uuid.UUID(dashboard_id)

    return database_root.dashboards['id', dashboard_id]


def find_by_url(url):
    """
    Returns a single Dashboard-entity with the given `url`, or None if it could not be found.
    :param url: The defining url for the dashboard we hope to find.
    :return: A single Dashboard-entity or None in case of failure.
    """
    return database_root.dashboards.get('url', url, default=None)


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

    # Clear current DB.
    database_root.dashboards = MultiIndexedPersistentCollection({'id', 'url'})

    # Fill in dashboards.
    _development_dashboards = [
        Dashboard(url='http://pydash.io/', user_id='000102030405060708090a0b0c0d0e0f'),
        Dashboard(url='http://pistach.io/', user_id='f0e0d0c0b0a090807060504030201000')
    ]
    for dashboard in _development_dashboards:
        print(f'Adding dashboard {dashboard}')
        add(dashboard)
    print('Seeding of dashboards is done!')
