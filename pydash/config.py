import os


class Config(object):
    SECRET_KEY = os.environ.get(
        'SECRET_KEY') or 'rigorous-security-will-be-implemented-post-MVP'

    # Mail configurations
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    #MAIL_DEBUG = True  # default = pydash_webapp.debug
    # MAIL_USERNAME       = 'noreply.PyDashTestMail@gmail.com'
    # MAIL_PASSWORD       = 'verysecurepydashpassword'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    DEFAULT_MAIL_SENDER = 'noreply-PyDashTestMail <noreply.pydashtestmail@gmail.com>'
