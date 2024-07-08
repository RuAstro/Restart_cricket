from flask import Flask, render_template, request, redirect, url_for
import logging

logging.basicConfig(
    filename="scorer.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

app = Flask(__name__)

batsman1 = {"name": "Batsman 1", "runs": 0, "balls": 0}
batsman2 = {"name": "Batsman 2", "runs": 0, "balls": 0}
total_runs = 0
current_batsman = batsman1

# Route to render the template initially
@app.route("/")
def index():
    logging.info("User accessed the cricket scorer page.")
    return render_template(
        "scorer_page.html",
        batsman1=batsman1,
        batsman2=batsman2,
        total_runs=total_runs,
        current_batsman=current_batsman["name"]
    )

# Route to handle adding runs
@app.route("/add_runs", methods=["POST"])
def add_runs():
    global total_runs, current_batsman

    runs = int(request.form["runs"])
    total_runs += runs

    current_batsman["runs"] += runs
    current_batsman["balls"] += 1

    # Determine which batsman is on strike
    if runs % 2 != 0:
        current_batsman = batsman2 if current_batsman == batsman1 else batsman1

    logging.info(
        f"Total runs updated to {total_runs}. Batsman1: {batsman1["runs"]}/{batsman1["balls"]}. Batsman2: {batsman2["runs"]}/{batsman2["balls"]}."
    )
    return redirect(url_for("index"))


# Route to handle adding wickets
@app.route("/add_wicket", methods=["POST"])
def add_wicket():
    logging.info("Wicket added.")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
