import uuid
from datetime import datetime, timezone, timedelta
import pydash_app.user.repository as repository
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
    user = repository.find_by_verification_code(verification_code)
    if user is None:
        # Could not find user with matching verification code.
        logger.warning(f"Verification code {verification_code} is invalid.")
        raise InvalidVerificationCodeError(f"Verification code {verification_code} is invalid.")

    if user.smart_verification_code.is_expired():
        # Throw away this verification code.
        user.smart_verification_code = None
        user.verification_code = None
        repository.update(user)
        logger.warning(f"Verification code {verification_code} has already expired.")
        raise VerificationCodeExpiredError(f"Verification code {verification_code} has already expired.")

    # Ensure verification code can be a string, an integer or a UUID object.
    if not isinstance(verification_code, uuid.UUID):
        verification_code = uuid.UUID(verification_code)

    if verification_code != user.verification_code:
        logger.warning(f"Verification codes do not match.")
        return False

    user.verified = True
    user.smart_verification_code = None
    user.verification_code = None
    repository.update(user)
    return True


class VerificationCode:
    """
    A 'smart' randomly generated verification code that keeps track of whether it has expired.
    Default expiration time is 7 days.
    """
    def __init__(self, expiration_time=timedelta(days=7)):
        self.verification_code = uuid.uuid4()
        self.expiration_datetime = datetime.now(tz=timezone.utc) + expiration_time

    def is_expired(self):
        return datetime.now(tz=timezone.utc) >= self.expiration_datetime


class VerificationCodeExpiredError(Exception):
    pass


class InvalidVerificationCodeError(Exception):
    pass
