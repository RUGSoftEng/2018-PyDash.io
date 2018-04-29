import uuid
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import flask_login
import persistent


class User(persistent.Persistent, flask_login.UserMixin):
    """
    The User entity knows about:

    - What properties a User has
    - What functionality makes sense to have this User interact with information from elsewhere.

    Per Domain Driven Design, it does _not_ contain information on how to persistently store/load a user!
    (That is instead handled by the `user_repository`).


    The User entity checks its parameters on creation:

    >>> User(42, 32)
    Traceback (most recent call last):
      ...
    TypeError
    """

    def __init__(self, name, password):
        if not isinstance(name, str) or not isinstance(password, str):
            raise TypeError("User expects name and password to be strings.")

        self.id = uuid.uuid4()
        self.name = name
        self.password_hash = generate_password_hash(password)
        self.verified = False
        self.verification_code = uuid.uuid4()

    def __repr__(self):
        """
        The user has a string representation to be easily introspectable:

        >>> user = User("Gandalf", "pass")
        >>> f"{user}".startswith("<User ")
        True
        """
        return '<{} id={} name={}>'.format(self.__class__.__name__, self.id, self.name)

    def get_id(self):
        return str(self.id)

    def get_verification_code(self):
        return str(self.verification_code)

    def is_verified(self):
        return self.verified

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Required because `multi_indexed_collection` puts users in a set, that needs to order its keys for fast lookup.
    # Because the IDs are unchanging integer values, use that.
    def __lt__(self, other):
        """
        Users are ordered. This is a requirement because the persistence layer will store them in a dictionary with ordered keys.

        The actual order does not matter, as long as the same object always has the same location.
        Therefore, we use the UUIDs for this.

        >>> gandalf = User("Gandalf", "pass")
        >>> dumbledore = User("Dumbledore", "secret")
        >>> gandalf < dumbledore or gandalf > dumbledore
        True
        >>> gandalf < gandalf
        False
        """
        return self.id < other.id
