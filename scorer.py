from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config["SECRET_KEY"] = "James_Bond"
bootstrap = Bootstrap(app)


@app.route("/")
def index():
    return render_template("scorer_page.html", runs=0, wickets=0)


@app.route("/add_runs/<int:runs>", methods=["POST"])
def add_runs(runs):
    current_runs = int(request.form.get("runs", 0))
    return str(current_runs + runs)


@app.route("/add_wicket", methods=["POST"])
def add_wicket():
    current_wickets = int(request.form.get("wickets", 0))
    return str(current_wickets + 1)


@app.route("/reset", methods=["POST"])
def reset():
    return "0"


if __name__ == "__main__":
    app.run(debug=True)
