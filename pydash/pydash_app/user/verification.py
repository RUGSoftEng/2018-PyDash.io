import uuid
from . import repository
import pydash_logger
from multi_indexed_collection import DuplicateIndexError


logger = pydash_logger.Logger(__name__)


def verify(verification_code):
    """
    Attempts to verify a user with the provided verification code.
    This is intended as a one-time action per user after registration.
    :param verification_code: The verification code that should match the User-entity's verification code.
        Can be a string or UUID object.
    :return: Returns True if both verification codes are equal, returns False otherwise.
        Raises an InvalidVerificationCodeError when the provided verification code is invalid.
        Raises an VerificationCodeExpiredError when the provided verification code has expired.
    """
    # Ensure verification code can be a string, an integer or a UUID object.
    if not isinstance(verification_code, uuid.UUID):
        verification_code = uuid.UUID(verification_code)

    user = repository.find_by_verification_code(verification_code)
    if user is None:
        # Could not find user with matching verification code.
        logger.warning(f"Verification code {verification_code} is invalid.")
        raise InvalidVerificationCodeError(f"Verification code {verification_code} is invalid.")

    if user.smart_verification_code.is_expired():
        # Throw away this verification code.
        # user.smart_verification_code = None
        # user.verification_code = None
        # # TODO: This won't work, as update(user) will now do nothing.
        # try:
        #     repository.update(user)
        # except DuplicateIndexError:
        #     pass  # We want to replace this on purpose. Sadly, this leaves the last verified user indexed with index 'None'.

        # TODO: Check if this goes well, w.r.t. pickling/persistance.
        delattr(user, 'verification_code')
        delattr(user, 'smart_verificaton_code')
        repository.update(user)  # TODO: check if repository.update() supports deleted attributes.

        logger.warning(f"Verification code {verification_code} has already expired.")
        raise VerificationCodeExpiredError(f"Verification code {verification_code} has already expired.")

    if verification_code != user.verification_code:
        logger.warning(f"Verification codes do not match.")
        return False

    user.verified = True
    # user.smart_verification_code = None
    # user.verification_code = None
    # # TODO: This won't work, as update(user) will now do nothing.
    # try:
    #     repository.update(user)
    # except DuplicateIndexError:
    #     pass  # We want to replace this on purpose. Sadly, this leaves the last verified user indexed with index 'None'.
    # Throw away this verification code.
    # TODO: Check if this goes well, w.r.t. pickling/persistance.
    delattr(user, 'verification_code')
    delattr(user, 'smart_verificaton_code')
    repository.update(user)  # TODO: check if repository.update() supports deleted attributes.
    return True


class VerificationCodeExpiredError(Exception):
    pass


class InvalidVerificationCodeError(Exception):
    pass
