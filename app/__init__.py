from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from app.telegram_bot import TelegramBot

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
telegram_bot = TelegramBot(Config.TELEGRAM_TOKEN)

from app import routes
assert routes
