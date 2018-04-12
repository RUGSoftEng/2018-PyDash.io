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
    For each user, stores some preliminary debug dashboards in the datastore,
    to be used during development.
    Note: for now the two dashboards that are being returned are
    identical, apart from the url.
    """

    from pydash_app.dashboard.dashboard import Dashboard
    from pydash_app.user import user_repository
    from pydash_app.dashboard.endpoint import Endpoint
    from pydash_app.dashboard.endpoint_call import EndpointCall
    from datetime import datetime, timedelta

    # Clear current Dashboards-DB.
    database_root.dashboards = MultiIndexedPersistentCollection({'id'})

    # # Fill in dashboards.
    # _dev_dashboard_urls = ['http://pydash.io/', 'http://pystach.io/']
    # _dev_endpoint_calls = [EndpointCall("foo", 0.5, datetime.now(), "0.1", "None", "127.0.0.1"),
    #                        EndpointCall("foo", 0.1, datetime.now(), "0.1", "None", "127.0.0.2"),
    #                        EndpointCall("bar", 0.2, datetime.now(), "0.1", "None", "127.0.0.1"),
    #                        EndpointCall("bar", 0.2, datetime.now() - timedelta(days=1), "0.1", "None", "127.0.0.1"),
    #                        EndpointCall("bar", 0.2, datetime.now() - timedelta(days=2), "0.1", "None", "127.0.0.1")
    #                        ]
    #
    # # Instead of storing the endpoints in a list, we generate them on the fly,
    # #  to avoid users sharing the same endpoints for now, as we'd like to have a controlled environment for every user
    # #  during this stage of development.
    # for user in user_repository.all():
    #     for url in _dev_dashboard_urls:
    #         dashboard = Dashboard(url, user.get_id())
    #         for endpoint in [Endpoint("foo", True), Endpoint("bar", True)]:
    #             dashboard.add_endpoint(endpoint)
    #         for endpoint_call in _dev_endpoint_calls:
    #             dashboard.add_endpoint_call(endpoint_call)
    #         print(f'Adding dashboard {dashboard}')
    #         add(dashboard)

    # TEST
    from pydash_app.fetching.dashboard_fetch import initialize_endpoints, initialize_endpoint_calls
    for user in user_repository.all():
        dashboard = Dashboard("http://136.243.248.188:9001/dashboard",
                              "cc83733cb0af8b884ff6577086b87909",
                              user.get_id())
        print(f'Adding dashboard {dashboard}')
        add(dashboard)
        print(f'Initialising dashboard {dashboard}')
        initialize_endpoints(dashboard)
        initialize_endpoint_calls(dashboard)

    print('Seeding of dashboards is done!')
