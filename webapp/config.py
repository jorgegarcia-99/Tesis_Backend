import os

class Config(object):
    DEBUG = False
    SECRET_KEY = 'dev'
    HOST = os.environ['ACCOUNT_HOST']
    MASTER_KEY = os.environ['ACCOUNT_KEY']
    DATABASE_ID = os.environ['COSMOS_DATABASE']



class DevelopmentConfig(Config):
    DEBUG = True
