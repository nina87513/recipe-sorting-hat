from db import db
import datetime


def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return value.strftime("%Y-%m-%d %H:%M:%S")


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(64), nullable=False)
    nickname = db.Column(db.String(50), nullable=False)

    def __init__(self, id, username, password, nickname):
        self.id = id
        self.username = username
        self.password = password
        self.nickname = nickname


class History(db.Model):
    __tablename__ = 'history'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    classification_results = db.Column(db.Integer, nullable=False)
    time = db.Column(db.DateTime(), nullable=False)
    username = db.Column(db.String(50), nullable=False)

    def __init__(self, classification_results, username):
        self.classification_results = classification_results
        self.time = datetime.datetime.now
        self.username = username
