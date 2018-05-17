import os


class Config(object):
    SECRET_KEY = os.environ.get(
        'SECRET_KEY') or 'rigorous-security-will-be-implemented-post-MVP'

    # Mail configurations
    # MAIL_SERVER = 'smtp.gmail.com'
    # MAIL_PORT = 465
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    # MAIL_USE_SSL = True
    #MAIL_DEBUG = True  # default = pydash_webapp.debug
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = 'noreply-PyDashTestMail <noreply.pydashtestmail@gmail.com>'
