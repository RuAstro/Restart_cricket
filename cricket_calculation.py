def calculate_strike_rate(batsman):
    """
    Calculate the strike rate of a batsman in cricket.

    Args:
        batsman (dict): Dictionary containing information about the batsman.
                        "runs" (int) and "balls" (int).

    Returns:
        float: Strike rate rounded to 2 decimal places.
    """
    if batsman["balls"] > 0:
        strike_rate = (batsman["runs"] / batsman["balls"]) * 100
        return round(strike_rate, 2)
    else:
        return 0.00


def calculate_current_run_rate(
    balls_faced: int, total_runs: int, total_overs: float
) -> float:
    """
    Calculate the current run rate in a cricket match.

    Args:
        balls_faced (int): Number of balls faced by the batting team.
        total_runs (int): Total runs scored by the batting team.
        total_overs (float): Total overs bowled in the match.

    Returns:
        float: Current run rate rounded to 2 decimal places.
    """
    if balls_faced > 0:
        overs = total_overs + (balls_faced // 6)
        balls_in_current_over = balls_faced % 6
        if balls_in_current_over > 0:
            overs += 1

        current_run_rate = total_runs / overs if overs > 0 else 0.00
        return round(current_run_rate, 2)
    else:
        return 0.00
