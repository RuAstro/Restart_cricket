from flask import Flask, render_template, request, redirect, url_for, flash
from dataclasses import dataclass
from models import db, Bowler, Balls
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


batsman1 = {"name": "Batsman 1", "runs": 0, "balls": 0}
batsman2 = {"name": "Batsman 2", "runs": 0, "balls": 0}
bowler_name = "Rabada"
total_runs = 0
current_batsman = batsman1
current_bowler = bowler_name
batsman_name = batsman1
runs_against_bowler = {bowler_name: 0}
total_overs = 0.0
balls_faced = 0
total_wickets = 0
previous_state = None

# Values to reset after each ball
current_runs = 0
current_wide_ball = False
current_no_ball = False
current_four_runs = False
current_six_runs = False


@dataclass
class Batsman:
    name: str
    runs: int = 0
    balls: int = 0


@dataclass
class Bowler:
    name: str
    runs_conceded: int = 0
    overs_bowled: float = 0.0
    wickets_taken: int = 0

    def total_cost(self) -> float:
        return self.unit_price * self.quantity_on_hand


# Route to render the template initially
@app.route("/")
def index():
    global total_runs, total_overs, balls_faced, total_wickets, current_batsman, bowler_name
    logging.info("User accessed the cricket scorer page.")
    return render_template(
        "scorer_page.html",
        batsman1=batsman1,
        batsman2=batsman2,
        total_runs=total_runs,
        current_batsman=current_batsman,
        bowler=bowler_name,
        runs_against_bowler=runs_against_bowler,
        strike_rate_batsman1=calculate_strike_rate(batsman1["runs"], batsman1["balls"]),
        strike_rate_batsman2=calculate_strike_rate(batsman2["runs"], batsman2["balls"]),
        current_run_rate=calculate_current_run_rate(
            balls_faced, total_runs, total_overs
        ),
        total_overs=total_overs,
        total_wickets=total_wickets,
        inning=is_inning_over(total_wickets),
        over_ended=True,
    )


# Route to handle adding runs
@app.route("/add_runs", methods=["POST"])
def add_runs():
    global total_runs, current_batsman, total_overs, balls_faced, runs_against_bowler, bowler_name

    runs = int(request.form["runs"])
    total_runs += runs

    # Update current batsman's runs and balls faced
    current_batsman["runs"] += runs
    current_batsman["balls"] += 1

    # Update the total balls faced
    balls_faced += 1

    # Determine which batsman is on strike
    if runs % 2 != 0:
        current_batsman = batsman2 if current_batsman == batsman1 else batsman1

    return redirect(url_for("index"))


# Route to handle update bowlers
@app.route("/update_bowler", methods=["POST"])
def update_bowler():
    global bowler_name, runs_against_bowler

    form_bowler_name = request.form.get("bowler", bowler_name)
    if form_bowler_name != bowler_name:
        bowler_name = form_bowler_name

    if bowler_name not in runs_against_bowler:
        runs_against_bowler[bowler_name] = 0

    return redirect(url_for("index"))


# Route to handle update overs
@app.route("/update_overs", methods=["POST"])
def update_overs():
    global total_overs

    # Increment overs when 6 balls are faced
    if balls_faced > 0 and balls_faced % 6 == 0:
        total_overs += 0.1

    return redirect(url_for("index"))


# Route to handle adding wickets
@app.route("/add_wicket", methods=["POST"])
def add_wicket():
    global total_wickets
    total_wickets += 1
    logging.info("Wicket added.")
    return redirect(url_for("index"))


# Route to handle for next ball
@app.route("/next_ball", methods=["POST"])
def next_ball(
    current_bowler=current_bowler,
    current_batsman=current_batsman["name"],
    current_runs=current_runs,
    current_no_ball=current_no_ball,
    current_wide_ball=current_wide_ball,
    current_four_runs=current_four_runs,
    current_six_runs=current_six_runs,
):
    # Create a new Balls entry for the current ball
    ball = Balls(
        bowler=current_bowler,
        batsman=current_batsman,
        runs=current_runs,
        no_ball=current_no_ball,
        wide_ball=current_wide_ball,
        four_runs=current_four_runs,
        six_runs=current_six_runs,
    )
    db.session.add(ball)
    db.session.commit()

    # Reset values for the next ball
    current_bowler = bowler_name
    current_batsman = batsman_name
    current_runs = 0
    current_wide_ball = False
    current_no_ball = False
    current_four_runs = False
    current_six_runs = False

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
