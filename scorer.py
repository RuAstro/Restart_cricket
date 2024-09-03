from flask import Flask, render_template, request, redirect, url_for
from models import db, Balls, Bowler, Batsman
from cricket_objects import BowlerData, BatsmanData, BallData
from cricket_calculation import (
    calculate_strike_rate,
    calculate_current_run_rate,
    is_inning_over,
)
import logging
import os
from checks import check_database


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


@app.route("/set_bowler", methods=["POST"])
def set_bowler():
    name = request.form.get("name")
    if name:
        bowler = Bowler.query.first()
        if bowler:
            bowler.name = name
        else:
            bowler = Bowler(name=name)
            db.session.add(bowler)
        db.session.commit()
        return redirect(url_for("index"))
    return redirect(url_for("index", error="Invalid name"))


# Fetch bowler data
@app.route("/get_bowler", methods=["GET"])
def get_bowler():
    bowler = Bowler.query.first()
    if bowler:
        return {"name": bowler.name}
    return {"name": None}


# Route to render the template initially
@app.route("/")
def index():
    # Fetch total runs, wickets, and overs
    total_runs = db.session.query(db.func.sum(Balls.runs)).scalar() or 0
    total_wickets = Balls.query.filter(Balls.wicket_taken == 1).count()
    total_balls = Balls.query.count()
    total_overs = (total_balls // 6) + (total_balls % 6) / 10

    # Calculate current run rate
    current_run_rate = total_runs / total_overs if total_overs > 0 else 0

    # Fetch batsman details
    batsman1_data = Balls.query.filter(Balls.batsman == batsman1.name).all()
    batsman2_data = Balls.query.filter(Balls.batsman == batsman2.name).all()

    # Calculate runs and balls faced for each batsman
    batsman1_runs = sum(ball.runs for ball in batsman1_data)
    batsman1_balls = len(batsman1_data)

    batsman2_runs = sum(ball.runs for ball in batsman2_data)
    batsman2_balls = len(batsman2_data)

    # Determine which batsman is on strike
    current_batsman = (
        batsman1.name if current_ball.batsman == batsman1.name else batsman2.name
    )

    # Fetch current bowler
    bowler_data = Balls.query.filter(Balls.bowler == bowler.name).all()

    bowler_runs = sum(ball.runs for ball in bowler_data)
    bowler_balls = len(bowler_data)

    inning = "First Inning" if total_runs < 100 else "Second Inning"

    # Render the template with all the required variables
    return render_template(
        "scorer_page.html",
        batsman1={
            "name": batsman1.name,
            "runs": batsman1_runs,
            "balls": batsman1_balls,
        },
        batsman2={
            "name": batsman2.name,
            "runs": batsman2_runs,
            "balls": batsman2_balls,
        },
        bowler={
            "name": bowler.name,
            "runs": bowler_runs,
            "balls": bowler_balls,
        },
        batsmen=batsmen,
        bowlers=bowlers,
        total_runs=total_runs,
        total_wickets=total_wickets,
        total_overs=total_overs,
        current_batsman=current_batsman,
        current_run_rate=current_run_rate,
        calculate_strike_rate=calculate_strike_rate,
        calculate_current_run_rate=calculate_current_run_rate,
        is_inning_ove=is_inning_over,
        inning=inning,
    )


# Route to handle adding runs
@app.route("/add_runs", methods=["POST"])
def add_runs():
    # Set current ball parameters based on request
    current_ball.runs = int(request.form.get("runs", 0))
    delivery_type = request.form.get("delivery_type", "normal")

    # Set attributes based on delivery type
    current_ball.four = delivery_type == "four_run"
    current_ball.six = delivery_type == "six_run"
    current_ball.no_ball = delivery_type == "no_ball"
    current_ball.wide = delivery_type == "wide"

    return process_next_ball(current_ball, delivery_type)


# Route to handle adding wickets
@app.route("/add_wicket", methods=["POST"])
def add_wicket():
    # Get the selected batsman from the form
    batsman = request.form.get("batsman")

    if batsman:
        current_ball.wicket_taken = True

        batsman1 = Batsman.query.filter_by(name=batsman).first()
        if batsman1:
            if current_ball.batsman == batsman1.name:
                if batsman2:
                    current_ball.batsman = batsman2.name
            else:
                current_ball.batsman = batsman1.name

        db.session.add(current_ball)
        db.session.commit()

    return redirect(url_for("index"))


# Route to handle for next ball
@app.route("/next_ball", methods=["POST"])
def next_ball():
    delivery_type = request.form.get("delivery_type", "normal")
    return process_next_ball(current_ball, delivery_type)


def process_next_ball(current_ball, delivery_type):
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
    # Calculate next batsman
    if current_ball.runs % 2 != 0:
        if current_ball.batsman == batsman1.name:
            current_ball.batsman = batsman2.name
        else:
            current_ball.batsman = batsman1.name

    # Reset current ball
    current_ball.reset()

    return redirect(url_for("index"))


if __name__ == "__main__":
    with app.app_context():
        db.init_app(app)
        db.create_all()
        check_database()

        # Fetch the first two Batsman
        batsman1 = Batsman.query.order_by(Batsman.id).limit(1).offset(0).first()
        batsman2 = Batsman.query.order_by(Batsman.id).limit(1).offset(1).first()
        bowler = Bowler.query.first()
        bowlers = [x.name for x in Bowler.query.all()]
        batsmen = [x.name for x in Batsman.query.all()]

        total_runs = 0
        total_overs = 0
        balls_faced = 0
        total_wickets = 0
        is_inning_over = False

        # Values to reset after each ball
        if batsman1 and bowler:
            current_ball = BallData(bowler=bowler.name, batsman=batsman1.name)

        app.run(debug=True)
