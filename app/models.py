import random
import string
from geoalchemy2 import Geometry
from sqlalchemy import func

from app import db


def encode_string(_string):
    if isinstance(_string, str):
        _string = _string.encode("utf-8")
    return _string


def get_random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))


def get_random_integer(length):
    numbers = '1234567890'
    return ''.join(random.choice(numbers) for i in range(length))


class Canalization(db.Model):
    __table_args__ = {'schema': 'blackbox'}

    id = db.Column(db.Integer, primary_key=True)
    geom = db.Column(Geometry())
    element_type = db.Column(db.String)
    description = db.Column(db.String)


class Rd008(db.Model):
    __table_args__ = {'schema': 'blackbox'}

    id = db.Column(db.Integer, primary_key=True)
    geom = db.Column(Geometry())
    description = db.Column(db.String)
    photo = db.Column(db.String)
    type = db.Column(db.String)
