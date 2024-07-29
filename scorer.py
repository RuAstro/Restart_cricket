from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Bowler, Balls
from cricket_objects import BowlerData, BatsmanData, BallData
from cricket_calculation import (
    calculate_strike_rate,
    calculate_current_run_rate,
    is_inning_over,
)
import logging
import os


logging.basicConfig(
    filename="scorer.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)


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
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


batsman1 = BatsmanData("batsman1")
batsman2 = BatsmanData("batsman2")
current_batsman = batsman1
bowler = BowlerData("Rabada")
total_runs: int = 0
total_overs: float = 0
balls_faced = 0
total_wickets = 0
previous_state = None

# Values to reset after each ball
current_ball = BallData(bowler=bowler.name, batsman=current_batsman.name)


# Route to render the template initially
@app.route("/")
def index(
    batsman1=batsman1,
    batsman2=batsman2,
    bowler=bowler,
    total_runs=total_runs,
    total_overs=total_overs,
):
    logging.info("User accessed the cricket scorer page.")
    return render_template(
        "scorer_page.html",
        batsman1=batsman1,
        batsman2=batsman2,
        total_runs=total_runs,
        current_batsman=batsman1,
        bowler=bowler.name,
        runs_against_bowler=bowler.runs_conceded,
        strike_rate_batsman1=calculate_strike_rate(batsman1.runs, batsman1.balls),
        strike_rate_batsman2=calculate_strike_rate(batsman2.runs, batsman2.balls),
        current_run_rate=calculate_current_run_rate(
            current_batsman.balls, total_runs, total_overs
        ),
        total_overs=total_overs,
        total_wickets=total_wickets,
        inning=is_inning_over(total_wickets),
        over_ended=True,
    )


# Route to handle adding runs
@app.route("/add_runs", methods=["POST"])
def add_runs(
    total_runs=total_runs, current_batsman=current_batsman, current_ball=current_ball
):
    runs = int(request.form["runs"])
    total_runs += runs

    # Update current batsman's runs and balls faced
    current_batsman.runs += runs
    current_batsman.balls += 1

    current_ball.runs = runs
    current_ball.batsman = current_batsman.name

    # Determine which batsman is on strike
    if runs % 2 != 0:
        current_batsman = batsman2 if current_batsman == batsman1 else batsman1

    return redirect(url_for("index"))


# Route to handle update bowlers
# @app.route("/update_bowler", methods=["POST"])
# def update_bowler():
#
#     form_bowler_name = request.form.get("bowler", bowler_name)
#     if form_bowler_name != bowler_name:
#         bowler_name = form_bowler_name
#
#     if bowler_name not in runs_against_bowler:
#         runs_against_bowler[bowler_name] = 0
#
#     return redirect(url_for("index"))
#


# Route to handle update overs
@app.route("/update_overs", methods=["POST"])
def update_overs(total_overs=total_overs):
    # Increment overs when 6 balls are faced
    if balls_faced > 0 and balls_faced % 6 == 0:
        total_overs += 0.1

    return redirect(url_for("index"))


# Route to handle adding wickets
@app.route("/add_wicket", methods=["POST"])
def add_wicket(total_wickets=total_wickets):
    total_wickets += 1
    logging.info("Wicket added.")
    return redirect(url_for("index"))


# Route to handle for next ball
@app.route("/next_ball", methods=["POST"])
def next_ball(current_ball=current_ball):
    current_ball.wide = bool(request.form["wide"])
    current_ball.no_ball = bool(request.form["no_ball"])
    current_ball.four = bool(request.form["four"])
    current_ball.six = bool(request.form["six"])
    # Create a new Balls entry for the current ball
    ball = Balls(
        bowler=current_ball.bowler,
        batsman=current_ball.batsman,
        runs=current_ball.runs,
        no_ball=current_ball.no_ball,
        wide_ball=current_ball.wide,
        four_runs=current_ball.four,
        six_runs=current_ball.six,
    )
    db.session.add(ball)
    db.session.commit()

    # Reset values for the next ball

    current_ball.reset()
    return redirect(url_for("index"))


# Route to handle undo button
@app.route("/undo", methods=["POST"])
def undo():
    if previous_state:
        batsman1 = previous_state["batsman1"]
        batsman2 = previous_state["batsman2"]
        bowler_name = previous_state["bowler_name"]
        total_runs = previous_state["total_runs"]
        total_wickets = previous_state["total_wickets"]
        total_overs = previous_state["total_overs"]

        # Clear previous state after undoing
        previous_state = None

    return redirect(url_for("index"))


if __name__ == "__main__":
    # initialize the app with the extension
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(debug=True)
