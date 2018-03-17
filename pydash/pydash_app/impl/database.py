import ZEO
import ZODB
import ZODB.FileStorage
import persistent
import BTrees.OOBTree
from multi_indexed_collection import MultiIndexedCollection

_db_address = 8090 # See the db_conf.zeoconf file for the correct port.
_connection = ZEO.connection(_db_address)

database_root = _connection.root

class MultiIndexedPersistentCollection(MultiIndexedCollection, persistent.Persistent):
    def __init__(self, properties):
        super().__init__(properties, dict_type=BTrees.OOBTree.BTree)
