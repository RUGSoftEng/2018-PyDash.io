import uuid
from datetime import datetime, timezone, timedelta

_DEFAULT_EXPIRATION_TIME = timedelta(days=1)


class VerificationCode:
    """
    A 'smart' randomly generated verification code that keeps track of whether it has expired.
    Default expiration time is one day.
    """
    def __init__(self, expiration_time=_DEFAULT_EXPIRATION_TIME):
        self.verification_code = uuid.uuid4()
        self.expiration_datetime = datetime.now(tz=timezone.utc) + expiration_time

    def is_expired(self):
        return datetime.now(tz=timezone.utc) >= self.expiration_datetime
