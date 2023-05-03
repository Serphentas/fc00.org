import os

class Config:
    REAL_IP_HEADER = 'x-real-ip'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('WEB_DB_URI')

    CJDNS_MAX_VERSION = 30

    NODE_DB_URI = os.environ.get('FC00_NODES_URI')