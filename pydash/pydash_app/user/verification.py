import uuid
from . import repository
import pydash_logger


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
        try:
            verification_code = uuid.UUID(verification_code)
        except ValueError:
            # Invalid input format
            logger.warning(f"Verification code {verification_code} is invalid - Invalid input format.")
            raise InvalidVerificationCodeError(f"Verification code {verification_code} is invalid.")

    user = repository.find_by_verification_code(verification_code)
    if user is None:
        # Could not find user with matching verification code.
        logger.warning(f"Verification code {verification_code} is invalid - Unable to find connected user.")
        raise InvalidVerificationCodeError(f"Verification code {verification_code} is invalid.")

    if user.smart_verification_code.is_expired():
        # Throw away this verification code.
        delattr(user, 'verification_code')
        delattr(user, 'smart_verification_code')
        repository.update(user)
        logger.warning(f"Verification code {verification_code} has already expired.")
        raise VerificationCodeExpiredError(f"Verification code {verification_code} has already expired.")

    user.verified = True
    # Throw away this verification code.
    delattr(user, 'verification_code')
    delattr(user, 'smart_verification_code')
    repository.update(user)


class VerificationCodeExpiredError(Exception):
    pass


class InvalidVerificationCodeError(Exception):
    pass
