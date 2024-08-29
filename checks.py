from models import db, Balls, Bowler, Batsman


def populate_batsmen():
    # Add default batsmen if none exist
    default_batsmen = [
        "Joe",
        "John",
        "RJ",
        "Jacob",
        "Frans",
        "Pieter",
        "Ox",
        "Malcolm",
        "Kolbe",
        "Markram",
        "Victor",
    ]
    existing_batsmen = {b.name for b in Batsman.query.all()}

    for name in default_batsmen:
        if name not in existing_batsmen:
            new_batsman = Batsman(name=name)
            db.session.add(new_batsman)
    db.session.commit()


def populate_bowlers():
    # Add default bowlers if none exist
    default_bowlers = [f"bowler{x}" for x in range(5)]
    existing_bowlers = {b.name for b in Bowler.query.all()}

    for name in default_bowlers:
        if name not in existing_bowlers:
            new_bowler = Bowler(name=name)
            db.session.add(new_bowler)
    db.session.commit()


def check_bowlers():
    """Check if there are no bowlers and call populate_bowlers if needed"""
    total_bowlers = Bowler.query.count()
    if total_bowlers == 0:
        populate_bowlers()


def check_batsmen():
    """Check if there are no batsmen and call populate_batsmen if needed"""
    total_batsmen = Batsman.query.count()
    if total_batsmen == 0:
        populate_batsmen()


def check_database():
    """Ensure batsmen and bowlers are populated"""
    check_batsmen()
    check_bowlers()
