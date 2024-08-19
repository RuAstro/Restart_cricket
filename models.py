from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Bowler(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    runs_conceded = db.Column(db.Integer, default=0)


class Balls(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bowler = db.Column(db.String(100), nullable=False)
    batsman = db.Column(db.String(100), nullable=False)
    runs = db.Column(db.Integer, default=0)
    no_ball = db.Column(db.Boolean, default=False)
    wide_ball = db.Column(db.Boolean, default=False)
    four_runs = db.Column(db.Boolean, default=False)
    six_runs = db.Column(db.Boolean, default=False)
    wicket_taken = db.Column(db.Boolean, default=False)
    # overs = db.Column(db.Float, default=0.0)


class GameStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_overs = db.Column(db.Float, default=0.0)
    balls_faced = db.Column(db.Integer, default=0)
