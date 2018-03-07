import app.model.datastore

class User:
    def __init__(self, name=None, password=None):
        if name == None or password == None:
            raise "Missing arguments to User constructor!"

        self.name = name
        self.password = password

    @classmethod
    def find_user_by_name(name):
        datastore.users.get(name)
