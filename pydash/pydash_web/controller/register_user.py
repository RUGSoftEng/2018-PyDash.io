"""
Manages the registration of a new user.
"""

from flask import jsonify
from flask_restplus.reqparse import RequestParser
from flask_mail import Message

from pydash_mail import mail

import pydash_app.user
import pydash_logger


logger = pydash_logger.Logger(__name__)

_MINIMUM_PASSWORD_LENGTH1 = 8
_MINIMUM_PASSWORD_LENGTH2 = 12


def register_user():
    args = _parse_arguments()

    username = args['username']
    password = args['password']
    email_address = args['email_address']

    print(f'args={args}')

    if not username or not password or not email_address:
        message = {'message': 'Username, password or email address missing'}
        logger.warning('User registration failed - username, password or email address missing')
        return jsonify(message), 400

    if not _check_password_requirements(password):
        message = {'message': 'User registration failed - password does not conform to the requirements.'}
        logger.warning('User registration failed - password does not conform to the requirements.')
        return jsonify(message), 400

    if pydash_app.user.find_by_name(username) is not None:
        message = {'message': f'User with username {username} already exists.'}
        logger.warning(f'While registering a user: {message}')
        return jsonify(message), 400
    else:
        user = pydash_app.user.User(username, password)
        pydash_app.user.add_to_repository(user)
        message = {'message': 'User successfully registered.',
                   'verification_code': f'{user.get_verification_code()}'}
        logger.info(f'User successfully registered with username: {username}'
                    f' and verification code {user.get_verification_code()}')

        _send_verification_email(user.get_verification_code(),
                                 user.get_verification_code_expiration_date(),
                                 email_address,
                                 user.name)
        return jsonify(message), 200


def _parse_arguments():
    parser = RequestParser()
    parser.add_argument('username')
    parser.add_argument('password')
    parser.add_argument('email_address')
    return parser.parse_args()


def _send_verification_email(verification_code, expiration_date, recipient_email_address, username):
    """
    Sends a verification email to the user with a link to the appropriate front-end page.
    For now the backend-api is directly given though.
    :param smart_verification_code: The verification code to send. Should be a VerificationCode instance.
    :param recipient_email_address: The email address of the recipient. Should be a string.
    :param username: The name of the User. Should be a string.
    """
    message_subject = 'PyDash.io - Account verification'
    message_recipients = [recipient_email_address]
    expiration_date = expiration_date.ctime() + ' GMT+0000'

    protocol = 'http'  # this or https  #Todo: change to https once that has been set up.
    host = 'localhost:5000'  # Todo: change from localhost to deployment server once that has been set up.
    verification_url = f'{protocol}://{host}/api/user/verify/{verification_code}'

    # Todo: perhaps read this in from a file, for flexibility.
    # Todo: still doesn't look all that great, but it will suffice for now.
    message_html = f'<p>Dear {username},</p>' \
                   f'<p>To verify your account, please click on this ' \
                   f'<a href=\"{verification_url}\">link</a>.' \
                   f'<br>(or copy and paste the following url into your internet browser and hit enter:' \
                   f' {verification_url} )</p>' \
                   f'<p>The link will expire at {expiration_date}.</p>'

    # No sender is specified, such that we use DEFAULT_MAIL_SENDER as specified in config.py
    message = Message(subject=message_subject,
                      recipients=message_recipients,
                      # body=message_body,
                      html=message_html
                      )

    mail.send(message)


def _check_password_requirements(password):
    rules1 = [lambda xs: any(x.isupper() for x in xs),
              lambda xs: any(not x.isalpha() for x in xs),
              lambda xs: len(xs) >= _MINIMUM_PASSWORD_LENGTH1
              ]
    rules2 = [lambda xs:len(xs) >= _MINIMUM_PASSWORD_LENGTH2]
    alternatives = [rules1, rules2]

    def func(rules):
        return all(rule(password) for rule in rules)

    return any(func(alternative) for alternative in alternatives)
