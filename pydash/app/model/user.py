import app.model.datastore

class User:
    def __init__(self, name=None, password=None):
        if name == None or password == None:
            raise "Missing arguments to User constructor!"

        self.name = name
        self.password = password

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.name)

    @classmethod
    def find_user_by_name(self,name):
        return app.model.datastore.load()['users'].get(name)
