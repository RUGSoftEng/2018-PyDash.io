import os

import ZEO
import persistent
import BTrees.OOBTree
from multi_indexed_collection import MultiIndexedCollection
import transaction


def _decide_database_address():
    """When "Testing" is an environment variable, an in-memory server is set up that will be gone after closing the process.
     Returns the address of that server, or the address as specified in the `db_config.zeoconf` file."""
    if "TESTING" in os.environ:
        address, stop = ZEO.server()  # <- in-memory server that's gone after closing of process.
        return address
    else:
        return ('127.0.0.1', 8091)  # <- As specified in the `db_config.zeoconf` file.


_database_address = _decide_database_address()
_database_connection = None
_current_process_id = None


def database_connection():
    """Sets up a database connection if it has not been set up yet in this process and returns said connection."""
    global _database_connection
    global _current_process_id
    if not _database_connection or os.getpid() != _current_process_id:
        _database_connection = ZEO.connection(_database_address)
        _current_process_id = os.getpid()
        transaction.begin()
        # print(f"PID {os.getpid()}: Created new DB connection: {_database_connection} connecting to {_database_address}")
    # else:
        # print(f"PID {os.getpid()}: Returning old DB connection {_database_connection}")
    return _database_connection


def database_root():
    """
    Returns the ZEO database root object.
    Wraps a database connection; a new connection is initialized once
    on each multiprocessing.Process.
    (on all subsequent calls on this process, the connection is re-used.)
    """
    return database_connection().root


class MultiIndexedPersistentCollection(MultiIndexedCollection, persistent.Persistent):
    def __init__(self, properties):
        super().__init__(properties, dict_type=BTrees.OOBTree.BTree)

