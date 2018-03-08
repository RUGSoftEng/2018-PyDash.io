import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'rigorous-security-will-be-implemented-post-MVP'
