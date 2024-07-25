from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


db = SQLAlchemy()


class Bowler(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)


class Balls(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bowler = db.Column(db.String(100), nullable=False)
    batsman = db.Column(db.String(100), nullable=False)
    runs = db.Column(db.Integer, default=0)
    no_ball = db.Column(db.Boolean, default=False)
    wide_ball = db.Column(db.Boolean, default=False)
    four_runs = db.Column(db.Boolean, default=False)
    six_runs = db.Column(db.Boolean, default=False)
