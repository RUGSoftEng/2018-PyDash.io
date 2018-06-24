"""
Fills the application with some preliminary users
to make it easier to test code in development and staging environments.
"""

from pydash_app.user.entity import User
import pydash_app.user.repository as repository


# TODO test this not in docstring perhaps?
def seed():
    """
    Stores some preliminary debug users in the datastore,
    to be used during development.

    >>> seed() #doctest: +ELLIPSIS
    Adding user <User id=... name=Alberto>
    Adding user <User id=... name=Arjan>
    Adding user <User id=... name=JeroenO>
    Adding user <User id=... name=JeroenL>
    Adding user <User id=... name=Koen>
    Adding user <User id=... name=Lars>
    Adding user <User id=... name=Patrick>
    Adding user <User id=... name=Tom>
    Adding user <User id=... name=W-M>
    Seeding of users is done!
    >>> found_user = repository.find_by_name("Alberto")
    >>> found_user.name == "Alberto"
    True
    """

    # Clear current DB.
    repository.clear_all()

    # Fill in users.
    _development_users = [
        User(name="Alberto", password="alberto", mail='some@email.com'),
        User(name="Arjan", password="arjan", mail='some@email.com'),
        User(name="JeroenO", password="jeroeno", mail='some@email.com'),
        User(name="JeroenL", password="jeroenl", mail='some@email.com'),
        User(name="Koen", password="koen", mail='some@email.com'),
        User(name="Lars", password="lars", mail='some@email.com'),
        User(name="Patrick", password="patrick", mail='some@email.com'),
        User(name="Tom", password="tom", mail='some@email.com'),
        User(name="W-M", password="topsecret", mail='some@email.com')
    ]
    for user in _development_users:
        user.verified = True
        print("Adding user {}".format(user))
        repository.add(user)
    print("Seeding of users is done!")
