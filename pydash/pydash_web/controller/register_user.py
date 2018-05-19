"""
Manages the registration of a new user.
"""

from flask import jsonify, request
from flask_mail import Message
from pydash_app.user.entity import check_password_requirements
from pydash_mail import mail

import pydash_app.user
import pydash_logger


logger = pydash_logger.Logger(__name__)


def register_user():
    request_data = request.get_json(silent=True)

    if not request_data:
        logger.warning('User registration failed - data missing')
        result = {'message': 'Data missing'}
        return jsonify(result), 400

    username = request_data.get('username')
    password = request_data.get('password')
    email_address = request_data.get('email_address')

    if username is None or password is None or email_address is None:
        logger.warning('User registration failed - username, password or email address missing')
        result = {'message': 'Username, password or email address missing'}
        return jsonify(result), 400

    # In case username, password or email_address are ''
    if not username or not password or not email_address:
        logger.warning('User registration failed - username, password or email address cannot be empty')
        result = {'message': 'Username, password or email address cannot be empty'}
        return jsonify(result), 400

    if not check_password_requirements(password):
        logger.warning('User registration failed - password does not conform to the requirements.')
        result = {'message': 'User registration failed - password does not conform to the requirements.'}
        return jsonify(result), 400

    if pydash_app.user.find_by_name(username) is not None:
        logger.warning(f'While registering a user: {message}')
        result = {'message': f'User with username {username} already exists.'}
        return jsonify(result), 400
    else:
        user = pydash_app.user.User(username, password)
        pydash_app.user.add_to_repository(user)
        
        logger.info(f'User successfully registered with username: {username}'
                    f' and verification code {user.get_verification_code()}')

        _send_verification_email(user.get_verification_code(),
                                 user.get_verification_code_expiration_date(),
                                 email_address,
                                 user.name)

        result = {'message': 'User successfully registered.',
                   'verification_code': f'{user.get_verification_code()}'}

        return jsonify(result), 200


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
