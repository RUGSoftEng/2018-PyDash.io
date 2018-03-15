import ZODB
import ZODB.FileStorage
import persistent
import BTrees.OOBTree
from multi_indexed_collection import MultiIndexedCollection

_storage = ZODB.FileStorage.FileStorage('zodb_filestorage.fs')
_db = ZODB.DB(_storage)
_connection = _db.open()

database_root = _connection.root

class MultiIndexedPersistentCollection(MultiIndexedCollection, persistent.Persistent):
    def __init__(self, properties):
        super().__init__(properties, dict_type=BTrees.OOBTree.BTree)
