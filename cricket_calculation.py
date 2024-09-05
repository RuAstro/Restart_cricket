def calculate_strike_rate(runs, balls):
    """
    Calculate the cricket strike rate based on runs scored and balls faced.

    The strike rate is a measure of how quickly a batsman scores runs. It is calculated as:
    (runs scored / balls faced) * 100

    Args:
        runs (int or float): The number of runs scored by the batsman.
        balls (int or float): The number of balls faced by the batsman.

    Returns:
        float: The strike rate of the batsman. If balls is 0, returns 0 to avoid division by zero.
    """
    if balls == 0:
        return 0
    return (runs / balls) * 100


def calculate_current_run_rate(balls, total_runs, total_overs):
    """
    Calculate the current run rate of a cricket match based on total runs and overs.

    The run rate is a measure of how many runs a team scores per over. It is calculated as:
    total_runs / total_overs

    Args:
        balls_faced (int): The number of balls bowled (not used in the calculation but included for completeness).
        total_runs (int): The total number of runs scored by the team.
        total_overs (int): The total number of overs bowled.

    Returns:
        float: The current run rate of the team. If total_overs is 0, returns 0 to avoid division by zero.
    """
    return total_runs / total_overs if total_overs > 0 else 0


def is_inning_over(total_wickets):
    """
    Determine if the cricket innings is over based on the number of wickets fallen.

    In cricket, an innings is typically considered over when a team has lost all 10 of its wickets.

    Args:
        total_wickets (int): The number of wickets that have fallen in the innings.

    Returns:
        bool: True if the innings is over (10 or more wickets have fallen), otherwise False.
    """
    return total_wickets >= 10
