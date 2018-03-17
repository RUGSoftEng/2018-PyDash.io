import uuid
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import flask_login
import persistent
import multi_indexed_collection


class User(persistent.Persistent, flask_login.UserMixin):
    """
    The User entitity knows about:

    - What properties a User has
    - What functionality makes sense to have this User interact with information from elsewhere.

    Per Domain Driven Design, it does _not_ contain information on how to persistently store/load a user!
    (That is instead handled by the `user_repository`).
    """

    def __init__(self, name, password):
        if not isinstance(name, str) or not isinstance(password, str):
            raise TypeError("User expects name and password to be strings.")

        self.id = uuid.uuid4() # str(id(self))
        self.name = name
        self.password_hash = generate_password_hash(password)

    def __repr__(self):
        return '<{} id={} name={}>'.format(self.__class__.__name__, self.id, self.name)

    # TODO Use an ID that is separate from the user's name.
    def get_id(self):
        return str(self.id)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


    def __lt__(self, other):
        self.id < other.id
