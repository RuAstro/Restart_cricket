from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


batsman1 = {"runs": 0, "balls": 0}
batsman2 = {"runs": 0, "balls": 0}
total_runs = 0


# Route to render the template initially
@app.route("/")
def index():
    return render_template(
        "scorer_page.html",
        batsman1=batsman1,
        batsman2=batsman2,
        total_runs=total_runs,
    )


# Route to handle adding runs
@app.route("/add_runs", methods=["POST"])
def add_runs():
    global total_runs
    runs = int(request.form["runs"])
    total_runs += runs

    # routs for the two batsmen
    if batsman1["balls"] <= batsman2["balls"]:
        batsman1["runs"] += runs
        batsman1["balls"] += 1
    else:
        batsman2["runs"] += runs
        batsman2["balls"] += 1

    return redirect(url_for("index"))


# Route to handle adding wickets
@app.route("/add_wicket", methods=["POST"])
def add_wicket():
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
