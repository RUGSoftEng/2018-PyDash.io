"""
This module handles the persistence of `Dashboard` entities:

It is an adapter of the actual persistence layer, to insulate the application
from datastore-specific details.

It handles a subset of the following tasks
(specifically, it only actually contains functions for the tasks the application needs in its current state!):

- Creating new entities of the specified type and finding them based on id.
>>> import pydash_app.dashboard.entity as dashboard
>>> import uuid
>>> dashboard = dashboard.Dashboard("", "", str(uuid.uuid4()))
>>> add(dashboard)
>>> found_dashboard = find(dashboard.get_id())
>>> found_dashboard.get_id() == dashboard.get_id()
True

- Asking for all dashboards is also possible!
>>> all() #doctest: +ELLIPSIS
<OOBTreeItems object at 0x...>

- Adding multiple instances of the same dashboard will return a KeyError or a DuplicateIndexError
TODO fix it so that it actually errors??
>>> import pydash_app.dashboard.entity as dashboard
>>> import uuid
>>> dashboard = dashboard.Dashboard("", "", str(uuid.uuid4()))
>>> add(dashboard)
>>> add(dashboard)


- Persisting updated versions of existing entities.
>>> import pydash_app.dashboard.entity as dashboard
>>> import uuid
>>> dashboard = dashboard.Dashboard("", "", str(uuid.uuid4()))
>>> add(dashboard)
>>> dashboard.token = "newToken"
>>> update(dashboard)
>>> found_dashboard = find(dashboard.get_id())
>>> found_dashboard.token == dashboard.token
True

- Deleting entities from the persistence layer, note that find() will return a KeyError if no dashboard was found.
>>> delete(dashboard)
>>> found_dashboard = find(dashboard.get_id())
Traceback (most recent call last):
    ...
KeyError

- Deleting non-existent dashboards will result in a KeyError.
>>> import pydash_app.dashboard.entity as dashboard
>>> import uuid
>>> dashboard = dashboard.Dashboard("", "", str(uuid.uuid4()))
>>> add(dashboard)
>>> delete(dashboard)
>>> delete(dashboard)
Traceback (most recent call last):
    ...
KeyError

"""
import uuid
import transaction
import pydash_logger
from pydash_database import database_root, MultiIndexedPersistentCollection
from multi_indexed_collection import DuplicateIndexError


logger = pydash_logger.Logger(__name__)


if not hasattr(database_root(), 'dashboards'):
    print("CREATING DASHBOARDS OBJECT")
    transaction.begin()
    database_root().dashboards = MultiIndexedPersistentCollection({'id'})
    transaction.commit()


def find(dashboard_id):
    """
    Find and retrieve the dashboard from the repository with id `dashboard_id`.
    :param dashboard_id: A string, integer or UUID instance representing the id of the dashboard in question.
    :return: A Dashboard instance if it is in the repository.
    :raises KeyError: If no dashboard with id `dashboard_id` is found in the repository.
    :raises Exception: If some internal error occurred.
    """
    # Ensure that this is also callable with strings or integers:
    if not isinstance(dashboard_id, uuid.UUID):
        dashboard_id = uuid.UUID(dashboard_id)
    logger.info(f"Starting to look for dashboard {dashboard_id}")

    try:
        res = database_root().dashboards['id', dashboard_id]
        logger.info(f"FOUND DASHBOARD in find_dashboard: {res}")
        return res
    except Exception as e:
        logger.error(f"EXCEPTION: {e}")
        raise


def all():
    """Returns an iterable collection of all dashboards in the repository (in no guaranteed order)."""
    return database_root().dashboards.values()


def add(dashboard):
    """
    Adds a dashboard to the repository.
    :param dashboard: The Dashboard instance to add to the repository.
    :raises (KeyError, DuplicateIndexError): When a dashboard with the same id already exists in the repository.
    """
    try:
        transaction.begin()
        database_root().dashboards.add(dashboard)
        transaction.commit()
    except (KeyError, DuplicateIndexError):
        transaction.abort()
        raise


def delete(dashboard):
    """
    Deletes a dashboard from the repository.
    :param dashboard: The Dashboard instance to delete from the repository.
    :raises KeyError: When the given dashboard does not exist within the repository.
    """
    try:
        transaction.begin()
        database_root().dashboards.remove(dashboard)
        transaction.commit()
    except KeyError:
        transaction.abort()
        raise


def update(dashboard):
    """
    Updates a dashboard in the repository with the values of the provided dashboard.
    :param dashboard: The Dashboard instance to update its counterpart in the repository with.
    """
    # Update item itself:
    transaction.commit()

    # Update indexes for item:
    for attempt in transaction.manager.attempts():
        with attempt:
            database_root().dashboards.update_item(dashboard)
    transaction.begin()


def clear_all():
    """Clears the entire repository."""
    transaction.begin()
    database_root().dashboards = MultiIndexedPersistentCollection({'id'})
    transaction.commit()
