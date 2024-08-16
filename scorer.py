from flask import Flask, render_template, request, redirect, url_for
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
def index():
    # Fetch total runs, wickets, and overs
    total_runs = db.session.query(db.func.sum(Balls.runs)).scalar() or 0
    total_wickets = Balls.query.filter(Balls.wicket_taken == 1).count()
    # total_overs = db.session.query(db.func.count(Balls.overs)).scalar()

    # Fetch current bowler
    bowler = Bowler.query.first()

    # Compute strike rates
    strike_rate_batsman1 = (
        (batsman1.runs / batsman1.balls * 100) if batsman1.balls > 0 else 0
    )
    strike_rate_batsman2 = (
        (batsman2.runs / batsman2.balls * 100) if batsman2.balls > 0 else 0
    )

    # Compute other stats
    current_run_rate = total_runs / total_overs if total_overs > 0 else 0
    required_run_rate = 0

    inning = "1st Innings"

    # Render the template with all the required variables
    return render_template(
        "scorer_page.html",
        batsman1=batsman1,
        batsman2=batsman2,
        total_runs=total_runs,
        total_wickets=total_wickets,
        total_overs=total_overs,
        bowler=bowler,
        strike_rate_batsman1=strike_rate_batsman1,
        strike_rate_batsman2=strike_rate_batsman2,
        current_run_rate=current_run_rate,
        required_run_rate=required_run_rate,
        inning=inning,
    )


# Route to handle adding runs
@app.route("/add_runs", methods=["POST"])
def add_runs(current_ball=current_ball):
    # Set current ball parameters based on request
    current_ball.runs = int(request.form.get("runs", 0))
    delivery_type = request.form.get("delivery_type", "normal")

    # Set attributes based on delivery type
    current_ball.four = delivery_type == "four_run"
    current_ball.six = delivery_type == "six_run"
    current_ball.no_ball = delivery_type == "no_ball"
    current_ball.wide = delivery_type == "wide"

    return next_ball(current_ball)


# Route to handle update overs
@app.route("/update_overs", methods=["POST"])
def update_overs(total_overs=total_overs):
    # Increment overs when 6 balls are faced
    if balls_faced > 0 and balls_faced % 6 == 0:
        total_overs += 0.1

    return redirect(url_for("index"))


# Route to handle adding wickets
@app.route("/add_wicket", methods=["POST"])
def add_wicket(current_ball=current_ball):

    # Create a new ball record with wicket taken
    current_ball.wicket_taken = True

    return redirect(url_for("index"))


# Route to handle for next ball
@app.route("/next_ball", methods=["POST"])
def next_ball(current_ball=current_ball):
    delivery_type = request.form.get("delivery_type", "normal")
    runs = current_ball.runs

    # Determine additional runs based on delivery type
    no_ball = delivery_type == "no_ball"
    wide_ball = delivery_type == "wide"
    four_runs = delivery_type == "four_run"
    six_runs = delivery_type == "six_run"

    # Calculate total runs including runs for special deliveries
    total_runs_to_add = runs
    if wide_ball or no_ball:
        total_runs_to_add += runs

    # Create a new Balls entry for the current ball
    ball = Balls(
        bowler=current_ball.bowler,
        batsman=current_ball.batsman,
        runs=total_runs_to_add,
        no_ball=no_ball,
        wide_ball=wide_ball,
        four_runs=four_runs,
        six_runs=six_runs,
        wicket_taken=current_ball.wicket_taken,
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
