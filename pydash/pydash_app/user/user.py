from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_login import UserMixin

class User(UserMixin):
    """
    The User entitity knows about:

    - What properties a User has
    - What functionality makes sense to have this User interact with information from elsewhere.

    Per Domain Driven Design, it does _not_ contain information on how to persistently store/load a user!
    (That is instead handled by the `user_repository`).
    """
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
