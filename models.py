from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


db = SQLAlchemy()


class Bowler(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    runs_given = db.Column(db.Integer, default=0)
    balls_bowled = db.Column(db.Integer, default=0)
    four_runs = db.Column(db.Integer, default=0)
    six_runs = db.Column(db.Integer, default=0)
    no_ball = db.Column(db.Integer, default=0)
    wide_ball = db.Column(db.Integer, default=0)


class Balls(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bowler = db.Column(db.String(100), nullable=False)
    runs = db.Column(db.Integer, default=0)
    no_ball = db.Column(db.Integer, default=0)
    wide_ball = db.Column(db.Integer, default=0)
