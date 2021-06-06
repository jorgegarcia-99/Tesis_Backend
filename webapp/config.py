import os

class Config(object):
    DEBUG = True
    SECRET_KEY = 'dev'
    DB_URI = 'mongodb://tesis-cosmos:LcCqbpwhQJAuswZIBlbCqVlGrxr5mpx2n77X8wuzpH24sUYNksMHLagP7gsLno5AosZxJFDJNZ8RSXs2nFjYCQ==@tesis-cosmos.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@tesis-cosmos@'


class DevelopmentConfig(Config):
    DEBUG = False
