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

    if pydash_app.user.find_by_name(username) is not None:
        message = {'message': f'User with username {username} already exists.'}
        logger.warning(f'While registering a user: {message}')
        return jsonify(message), 409  # Todo: perhaps return 400 instead?
    else:
        user = pydash_app.user.User(username, password)
        pydash_app.user.add_to_repository(user)
        message = {'message': 'User successfully registered.',
                   'verification_code': f'{user.get_verification_code()}'}
        logger.info(f'User successfully registered with username: {username}'
                    f' and verification code {user.get_verification_code()}')

        logger.info(f'user {user} to be found with vc {user.verification_code}:'
                    f' {pydash_app.user.find_by_verification_code(user.verification_code)}')

        _send_verification_email(user.smart_verification_code.verification_code,
                                 user.smart_verification_code.expiration_datetime,
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
    message_subject = 'PyDash.io - Account verification'
    message_recipients = [recipient_email_address]
    # message_body = f'Dear {username},'
    verification_url = f'localhost:5000/api/user/verify/{verification_code}'  # Todo: change from localhost to deployment server once that has been set up.

    # TODO: make this proper html
    message_html = f'Dear {username},\n\n' \
                   f'To verify your account, please click on this ' \
                   f'<a href="{verification_url}"link</a>.\n' \
                   f'(or copy and paste the following url into your internet browser and hit enter:' \
                   f' {verification_url} )\n\n' \
                   f'The link will expire at {expiration_date}.'  # Todo: make this datetime object format look nicer.
    message_sender = 'no-reply_PyDashTestMail@gmail.com'

    message = Message(subject=message_subject,
                      recipients=message_recipients,
                      # body=message_body,
                      html=message_html,
                      sender=message_sender
                      )

    mail.send(message)
