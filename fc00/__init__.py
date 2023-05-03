from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from fc00.config import Config

APP = Flask(__name__)
APP.config.from_object(Config)

with APP.app_context():
    DB = SQLAlchemy(APP)
    from fc00.models import *
    DB.create_all()

import fc00.views