def calculate_strike_rate(runs, balls):
    if balls == 0:
        return 0
    return (runs / balls) * 100


def calculate_current_run_rate(balls, total_runs, total_overs):
    return total_runs / total_overs if total_overs > 0 else 0


def is_inning_over(total_wickets):
    return total_wickets >= 10
