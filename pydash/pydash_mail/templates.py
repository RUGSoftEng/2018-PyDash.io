"""
Reads mail templates into memory and provides functions to format them.
"""

with open('mail_templates/verification_html.txt', 'r') as f:
    _verification_mail_html = f.read()

with open('mail_templates/verification_plain.txt', 'r') as f:
    _verification_mail_plain = f.read()


def format_verification_mail_html(username, verification_url, expiration_date):
    """
    Format an HTML verification mail.
    :param username: Username to use in the mail.
    :param verification_url: Verification link to use in the mail.
    :param expiration_date: Expiration date of the verification code.
    :return: The formatted HTML verification mail.
    """
    return _verification_mail_html.format(username=username,
                                          verification_url=verification_url,
                                          expiration_date=expiration_date)


def format_verification_mail_plain(username, verification_url, expiration_date):
    """
    Format a plaintext verification mail.
    :param username: Username to use in the mail.
    :param verification_url: Verification link to use in the mail.
    :param expiration_date: Expiration date of the verification code.
    :return: The formatted plaintext verification mail.
    """
    return _verification_mail_plain.format(username=username,
                                           verification_url=verification_url,
                                           expiration_date=expiration_date)
