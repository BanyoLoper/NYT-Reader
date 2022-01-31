from .app import app
from flask import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON

db = SQLAlchemy(app)

class Token(db.Model):
    __tablename__ = 'api_connections'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String())
    value = db.Column(db.String())

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self) -> str:
        return '<id {}>'.format(self.id)