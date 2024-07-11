from flask import Flask, render_template, request, redirect, url_for, flash
import logging
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
import os
from cricket_calculation import calculate_strike_rate, calculate_current_run_rate


class Base(DeclarativeBase):
    pass


logging.basicConfig(
    filename="scorer.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

db = SQLAlchemy(model_class=Base)
# create the app
app = Flask(__name__)
# Secret Key
app.secret_key = "James Bond"
# Get the absolute path to the directory where this script is located
basedir = os.path.abspath(os.path.dirname(__file__))
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir, "tracking.db"
)


batsman1 = {"name": "Batsman 1", "runs": 0, "balls": 0}
batsman2 = {"name": "Batsman 2", "runs": 0, "balls": 0}
total_runs = 0
current_batsman = batsman1
bowler = "Rabada"
runs_against_bowler = {bowler: 0}
total_overs = 0.0
balls_faced = 0
total_wickets = 0


class Teams(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    table_ranked = db.Column(db.Integer, default=0)


class Batsman(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    runs = db.Column(db.Integer, default=0)
    balls_faced = db.Column(db.Integer, default=0)
    strike_rate = db.Column(db.Integer, default=0)


class Bowler(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    runs_given = db.Column(db.Integer, default=0)
    balls_bowled = db.Column(db.Integer, default=0)


def end_inning():
    if total_wickets > 9:
        return "End Of Inning"
    else:
        return "First Inning"


# Route to render the template initially
@app.route("/")
def index():
    global total_runs, total_overs, balls_faced, total_wickets
    logging.info("User accessed the cricket scorer page.")
    return render_template(
        "scorer_page.html",
        batsman1=batsman1,
        batsman2=batsman2,
        total_runs=total_runs,
        current_batsman=current_batsman["name"],
        bowler=bowler,
        runs_against_bowler=runs_against_bowler,
        strike_rate_batsman1=calculate_strike_rate(batsman1),
        strike_rate_batsman2=calculate_strike_rate(batsman2),
        current_run_rate=calculate_current_run_rate(
            balls_faced, total_runs, total_overs
        ),
        total_overs=total_overs,
        total_wickets=total_wickets,
        inning=end_inning(),
    )


# Route to handle adding runs
@app.route("/add_runs", methods=["POST"])
def add_runs():
    global total_runs, current_batsman, total_overs, balls_faced

    runs = int(request.form["runs"])
    total_runs += runs

    current_batsman["runs"] += runs
    current_batsman["balls"] += 1

    balls_faced += 1

    # Determine which batsman is on strike
    if runs % 2 != 0:
        current_batsman = batsman2 if current_batsman == batsman1 else batsman1

    bowler_name = request.form.get("bowler", "")
    bowler = Bowler.query.filter_by(name=bowler_name).first()
    if bowler:
        bowler.runs_given += runs
        bowler.balls_bowled += 1
    else:
        # Create a new bowler entry if not exists
        bowler = Bowler(name=bowler_name, runs_given=runs, balls_bowled=1)
        db.session.add(bowler)

    if balls_faced % 6 == 0:
        total_overs += 1
        # Switch batsmen after completing an over
        current_batsman = batsman2 if current_batsman == batsman1 else batsman1

    db.session.commit()

    logging.info(
        f"Total runs updated to {total_runs}. Batsman1: {batsman1['runs']}/{batsman1['balls']}. Batsman2: {batsman2['runs']}/{batsman2['balls']}."
    )
    return redirect(url_for("index"))


# Route to handle adding wickets
@app.route("/add_wicket", methods=["POST"])
def add_wicket():
    global total_wickets
    total_wickets += 1
    logging.info("Wicket added.")
    return redirect(url_for("index"))


if __name__ == "__main__":
    # initialize the app with the extension
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(debug=True)
