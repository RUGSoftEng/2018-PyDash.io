"""
This module is the public interface (available to the web-application pydash_web)
for interacting with Users.


Example Usage:

>>> gandalf = User("Gandalf", "pass", 'some@email.com')
>>> add_to_repository(gandalf)
...
>>> found_user = find(gandalf.id)
>>> found_user.name == "Gandalf"
True

You can also use a string-version of the ID to find the user again:

>>> found_user = find(str(gandalf.id))
>>> found_user.name == "Gandalf"
True


>>> found_user2 = find_by_name("Gandalf")
>>> found_user2 == found_user
True
>>> find_by_name("Dumbledore")
>>> # ^Returns nothing
>>> res_user = authenticate("Gandalf", "pass")
>>> res_user.name == "Gandalf"
True
>>> authenticate("Gandalf", "youshallnot")
>>> # ^Returns nothing
>>> authenticate("Dumbledore", "secrets")
>>> # ^Returns nothing
"""
from .entity import User
from . import repository
from . import verification
from multi_indexed_collection import DuplicateIndexError

_MINIMUM_PASSWORD_LENGTH1 = 8
_MINIMUM_PASSWORD_LENGTH2 = 12


def add_to_repository(user):
    """
    Adds the given User-entity to the user_repository. Raises a KeyError if the user is already in the repository.
    :param user: The User-entity in question.

    Adding the same user twice with the same name is not allowed:

    >>> gandalf1 = User("Gandalf", "pass", 'some@email.com')
    >>> add_to_repository(gandalf1)
    >>> gandalf2 = User("Gandalf", "balrog", 'some@email.com')
    >>> add_to_repository(gandalf2)
    Traceback (most recent call last):
      ...
    multi_indexed_collection.DuplicateIndexError

    """
    try:
        repository.add(user)
    except (KeyError, DuplicateIndexError):
        raise


def remove_from_repository(user_id):
    """
    Removes the User-entity whose user_id is `user_id` from the repository.

    >>> gandalf1 = User("Gandalf", "pass", 'some@email.com')
    >>> add_to_repository(gandalf1)
    >>> remove_from_repository(gandalf1.get_id())
    >>> found_user = find_by_name("Gandalf")
    >>> found_user == None
    True

    Will raise a KeyError if said user is not in the repository.

    >>> gandalf1 = User("Gandalf", "pass", 'some@email.com')
    >>> add_to_repository(gandalf1)
    >>> remove_from_repository(gandalf1.get_id())
    >>> remove_from_repository(gandalf1.get_id())
    Traceback (most recent call last):
      ...
    KeyError

    :param user_id: The ID of the User-entity to be removed. This can be either a UUID-entity or the corresponding
        string representation.
    """
    try:
        repository.delete_by_id(user_id)
    except KeyError:
        raise


def find(user_id):
    """
    Returns a single User-entity with the given UUID or None if it could not be found.
    :param user_id: The ID of the User-entity to be removed. This can be either a UUID-entity or the corresponding
        string representation.
    """
    return repository.find(user_id)


def maybe_find_user(user_id):
    """
    Returns the User entity, or `None` if it does not exist.
    :param user_id: The ID of the User-entity to be removed. This can be either a UUID-entity or the corresponding
        string representation.

    >>> user = User("Gandalf", "pass", 'some@email.com')
    >>> add_to_repository(user)
    ...
    >>> found_user = maybe_find_user(user.id)
    >>> found_user.name == "Gandalf"
    True
    >>> import uuid
    >>> unexistent_uuid = uuid.UUID('ced84534-7a55-440f-ad77-9912466fe022')
    >>> unexistent_user = maybe_find_user(unexistent_uuid)
    >>> unexistent_user == None
    True
    """
    try:
        return find(user_id)
    except KeyError:
        return None


def find_by_name(name):
    """
    Returns a single User-entity with the given `name`, or None if it could not be found.

    :param name: Name of the user we hope to find.
    """
    return repository.find_by_name(name)


def find_by_verification_code(verification_code):
    """
    Returns a single User-entity with the given `verification_code`, or None if it could not be found.
    :param verification_code: The verification code of the user we hope to find.
    """
    return repository.find_by_verification_code(verification_code)


def authenticate(name, password):
    """
    Attempts to authenticate the user with name `name`
    and password `password`.

    :param name: A string indicating the user's name.
    :param password: A string indicating the user's password.
    :returns: Returns the user object. If authentication fails (unknown user or incorrect password), returns None.
    """
    maybe_user = find_by_name(name)
    if maybe_user is None or not maybe_user.check_password(password):
        return None
    return maybe_user


def verify(verification_code):
    """
        Attempts to verify a user with the provided verification code.
        This is intended as a one-time action per user after registration.
        :param verification_code: The verification code that should match the User-entity's verification code.
            Can be a string or UUID object.
        :raises InvalidVerificationCodeError: When the provided verification code is invalid.
        :raises VerificationCodeExpiredError: When the provided verification code has expired.
        """
    verification.verify(verification_code)


def check_password_requirements(password):
    f"""
    Checks whether the given password conforms to at least one set of rules in the following series of alternative requirements:
     - Password contains at least one upper-case character, at least one non-alphabetical character and is at least
       {_MINIMUM_PASSWORD_LENGTH1} characters long.
     - Password is at least {_MINIMUM_PASSWORD_LENGTH2} characters long.

    :param password: A string denoting the password to check.
    :return: Whether the password conforms to at least one set of the above mentioned rules.
    """
    rules1 = [
        lambda xs: any(x.isupper() for x in xs),
        lambda xs: any(not x.isalpha() for x in xs),
        lambda xs: len(xs) >= _MINIMUM_PASSWORD_LENGTH1
    ]
    rules2 = [
        lambda xs: len(xs) >= _MINIMUM_PASSWORD_LENGTH2
    ]
    alternatives = [rules1, rules2]

    def check_rules(rules):
        return all(rule(password) for rule in rules)

    return any(check_rules(alternative) for alternative in alternatives)
