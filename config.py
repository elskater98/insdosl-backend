import os
import datetime

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('HACKEPS_DATABASE_URI') or ''
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_recycle": 3600,
    }

    TELEGRAM_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
    TELEGRAM_NOTIFICATION_USERS = '19405938'
