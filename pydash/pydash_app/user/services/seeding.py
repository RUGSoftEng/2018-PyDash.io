"""
Fills the application with some preliminary users
to make it easier to test code in development and staging environments.
"""

from pydash_app.user.user import User
import pydash_app.user.repository as repository


def seed():
    """
    Stores some preliminary debug users in the datastore,
    to be used during development.
    """

    # Clear current DB.
    repository.clear_all()

    # Fill in users.
    _development_users = [
        User(name="Alberto", password="alberto"),
        User(name="Arjan", password="arjan"),
        User(name="JeroenO", password="jeroeno"),
        User(name="JeroenL", password="jeroenl"),
        User(name="Koen", password="koen"),
        User(name="Lars", password="lars"),
        User(name="Patrick", password="patrick"),
        User(name="Tom", password="tom"),
        User(name="W-M", password="topsecret")
    ]
    for user in _development_users:
        print("Adding user {}".format(user))
        repository.add(user)
    print("Seeding of users is done!")
