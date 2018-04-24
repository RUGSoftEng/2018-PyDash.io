import os

import ZEO
import persistent
import BTrees.OOBTree
from multi_indexed_collection import MultiIndexedCollection



def _decide_database_address():
    if os.environ.get("TEST"):
        address, stop = ZEO.server() # <- in-memory server that's gone after closing of process.
        return address
    else:
        return ('127.0.0.1', 8091) # <- As specified in the `db_config.zeoconf` file.


_database_address = _decide_database_address()
_database_root = None
_current_process_id = None

def database_root():
    """
    Returns the ZEO database root object.
    Wraps a database connection; a new connection is initialized once
    on each multiprocessing.Process.
    (on all subsequent calls on this process, the connection is re-used.)
    """
    global _database_root
    global _current_process_id
    if not _database_root or os.getpid() != _current_process_id:
        _connection = ZEO.connection(_database_address)
        _database_root = _connection.root
        _current_process_id = os.getpid()
        print(f"PID {os.getpid()}: Created new DB connection: {_connection} connecting to {_database_address} {_database_root}")
    else:

        print(f"PID {os.getpid()}: returning old connection {_database_root}")
    return _database_root

class MultiIndexedPersistentCollection(MultiIndexedCollection, persistent.Persistent):
    def __init__(self, properties):
        super().__init__(properties, dict_type=BTrees.OOBTree.BTree)

