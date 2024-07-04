from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config["SECRET_KEY"] = "James_Bond"
bootstrap = Bootstrap(app)


@app.route("/")
def index():
    return render_template("scorer_page.html", runs=0, wickets=0)


@app.route("/add_runs", methods=["POST"])
def add_runs():
    runs = int(request.form.get("runs", 0))
    return str(runs)


@app.route("/add_wicket", methods=["POST"])
def add_wicket():
    wickets = int(request.form.get("wickets", 0))
    return str(wickets + 1)


if __name__ == "__main__":
    app.run(debug=True)
