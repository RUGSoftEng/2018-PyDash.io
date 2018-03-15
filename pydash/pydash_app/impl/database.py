import ZODB
import ZODB.FileStorage

_storage = ZODB.FileStorage.FileStorage('zodb_filestorage.fs')
_db = ZODB.DB(_storage)
_connection = _db.open()

database_root = _connection.root
