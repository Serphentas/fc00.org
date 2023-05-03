from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from web.config import Config

APP = Flask(__name__)
APP.config.from_object(Config)

with APP.app_context():
    DB = SQLAlchemy(APP)
    from web.models import *
    DB.create_all()

import web.views