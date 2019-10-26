import os

from sensitive_config import SensitiveConfig


basedir = os.path.abspath(os.path.dirname(__file__))

class Config(SensitiveConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 64 * 1024
