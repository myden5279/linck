from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    head = db.Column(db.String(100))
    body = db.Column(db.String(10000))
    images = db.Column(db.String(10000))
    date = db.Column(db.DateTime, default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    identifier = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    posts = db.relationship('Posts')
