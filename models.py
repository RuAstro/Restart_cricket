from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, Float

db = SQLAlchemy()


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class Teams:
    """
    SQLAlchemy model for storing information about teams.

    Attributes:
        id (int): Primary key identifier for the team.
        name (str): Name of the team.
        table_ranked (int): Ranking of the team in a table.

    Args:
        Base (): Base class for SQLAlchemy declarative models.
    """

    __tablename__ = "teams"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    table_ranked = Column(Integer, default=0)


class Batsman:
    """
    SQLAlchemy model for storing information about batsmen.

    Attributes:
        id (int): Primary key identifier for the batsman.
        name (str): Name of the batsman.
        runs (int): Total runs scored by the batsman.
        balls_faced (int): Total balls faced by the batsman.
        strike_rate (float): Strike rate of the batsman.

    Args:
        Base (): Base class for SQLAlchemy declarative models.
    """

    __tablename__ = "batsman"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    runs = Column(Integer, default=0)
    balls_faced = Column(Integer, default=0)
    strike_rate = Column(Float, default=0)


class Bowler(db.Model):
    """
    SQLAlchemy model for storing information about bowlers.

    Attributes:
        id (int): Primary key identifier for the bowler.
        name (str): Name of the bowler.
        runs_given (int): Total runs conceded by the bowler.
        balls_bowled (int): Total balls bowled by the bowler.

    Args:
        Base (): Base class for SQLAlchemy declarative models.
    """

    __tablename__ = "bowlers"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    runs_given = Column(Integer, default=0)
    balls_bowled = Column(Integer, default=0)


class Balls(db.Model):
    id = Column(Integer, primary_key=True)
    run_per_ball = Column(String(100), nullable=False)
    wide_ball = Column(Integer, default=0)
    no_ball = Column(Integer, default=0)
