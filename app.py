from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
import os


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
# create the app
app = Flask(__name__)
# Get the absolute path to the directory where this script is located
basedir = os.path.abspath(os.path.dirname(__file__))
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "test.db")


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    runs = db.Column(db.Integer, nullable=False)
    balls = db.Column(db.Integer, nullable=False)
    strike_rate = db.Column(db.Float)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/calculate", methods=["POST"])
def calculate():
    runs = int(request.form["runs"])
    balls = int(request.form["balls"])

    if balls > 0:
        strike_rate = (runs / balls) * 100
    else:
        strike_rate = 0.0

    new_player = Player(name="Player", runs=runs, balls=balls, strike_rate=strike_rate)
    db.session.add(new_player)
    db.session.commit()

    return redirect(url_for("result", strike_rate=strike_rate))


@app.route("/result/<float:strike_rate>")
def result(strike_rate):
    return render_template("result.html", strike_rate=strike_rate)


if __name__ == "__main__":
    # initialize the app with the extension
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(debug=True)
