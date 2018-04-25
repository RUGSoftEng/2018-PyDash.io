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
import pydash_app.impl.database


if not hasattr(database_root(), 'dashboards'):
    transaction.begin()
    database_root().dashboards = MultiIndexedPersistentCollection({'id'})
    transaction.commit()


print(f"DASHBOARDS: {list(database_root().dashboards.values())}")

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
    transaction.begin()
    database_root().dashboards = MultiIndexedPersistentCollection({'id'})
    transaction.commit()

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
    # from pydash_app.fetching.fetching import fetch_and_add_endpoints, fetch_and_add_historic_endpoint_calls
    import pydash_app.dashboard.services.fetching as fetching
    #for user in user_repository.all():
    for user in [user_repository.find_by_name('W-M'), user_repository.find_by_name('Koen')]:
        dashboard = Dashboard("http://136.243.248.188:9001/dashboard",
                              "cc83733cb0af8b884ff6577086b87909",
                              user.get_id())
        print(f'Adding dashboard {dashboard}')
        add(dashboard)
        print(f'Fetching remote info for dashboard {dashboard}.')
        fetching.fetch_historic_dashboard_info(dashboard.id)
        # fetching.fetch_and_add_endpoints(dashboard)
        # fetching.fetch_and_add_historic_endpoint_calls(dashboard)

        print(f'- {len(dashboard.endpoints)} endpoints found')
        print(f'- {len(dashboard._endpoint_calls)} historical endpoint calls')
        update(dashboard)
        print(f'Initialized dashboard')
        print(f'- {len(dashboard.endpoints)} endpoints found')
        print(f'- {len(dashboard._endpoint_calls)} historical endpoint calls')

    print('Seeding of dashboards is done!')
