from dataclasses import dataclass


@dataclass
class BallData:
    bowler: str
    batsman: str
    runs: int = 0
    four: bool = False
    six: bool = False
    wide: bool = False
    no_ball: bool = False
    wicket_taken: bool = False
    balls_in_over: int = 0

    def reset(self):
        """Reset ball data for the next delivery."""
        self.runs = 0
        self.four = False
        self.six = False
        self.wide = False
        self.no_ball = False
        self.wicket_taken = False
        self.balls_in_over = 0


@dataclass
class BatsmanData:
    name: str
    runs: int = 0
    balls: int = 0


@dataclass
class BowlerData:
    name: str
    runs_conceded: int = 0
    overs_bowled: float = 0.0
    wickets_taken: int = 0

    def total_cost(self) -> float:
        return self.unit_price * self.quantity_on_hand
