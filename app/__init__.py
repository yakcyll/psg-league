from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

app = Flask(__name__, template_folder='../templates')
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

from app import routes, models, errors

import logging
from logging.handlers import RotatingFileHandler
import os

if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')

    __file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
    __file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s%(lineno)d]'))
    __file_handler.setLevel(logging.INFO)
    app.logger.addHandler(__file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('PSG League app start-up')
