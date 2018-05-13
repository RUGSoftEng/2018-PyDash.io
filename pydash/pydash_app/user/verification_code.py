import uuid
from datetime import datetime, timezone, timedelta


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
