from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_login import UserMixin

import app.model.datastore

class User(UserMixin):
    def __init__(self, name=None, password=None):
        if name == None or password == None:
            raise "Missing arguments to User constructor!"

        self.id = str(id(self))
        self.name = name
        self.password_hash = generate_password_hash(password)

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self.name)

    # TODO Use an ID that is separate from the user's name.
    def get_id(self):
        return self.name

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def find_user_by_name(self, name):
        return app.model.datastore.load()['users'].get(name)
