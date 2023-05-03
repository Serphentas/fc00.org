import os

class Config:
    DEBUG = False

    REAL_IP_HEADER = 'x-real-ip'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('WEB_DB_URI')
