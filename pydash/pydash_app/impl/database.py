import ZEO
import persistent
import BTrees.OOBTree
from multi_indexed_collection import MultiIndexedCollection

_database_port = 8091 # <- As specified in the `db_config.zeoconf` file.
_database_root = None
_current_process_id = None

def database_root():
    """
    Returns the ZEO database root object.
    Wraps a database connection; a new connection is initialized once
    on each multiprocessing.Process.
    (on all subsequent calls on this process, the connection is re-used.)
    """
    import os
    global _database_root
    global _current_process_id
    if not _database_root or os.getpid() != _current_process_id:
        _connection = ZEO.connection(_database_port)
        _database_root = _connection.root
        _current_process_id = os.getpid()
    return _database_root

class MultiIndexedPersistentCollection(MultiIndexedCollection, persistent.Persistent):
    def __init__(self, properties):
        super().__init__(properties, dict_type=BTrees.OOBTree.BTree)

