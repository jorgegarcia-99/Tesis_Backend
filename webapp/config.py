import os

class Config(object):
    DEBUG = True
    SECRET_KEY = 'dev'
    DB_URI = os.environ['DATABASE_SERVER']


class DevelopmentConfig(Config):
    DEBUG = False
