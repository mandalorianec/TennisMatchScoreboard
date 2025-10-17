from dataclasses import dataclass


@dataclass
class MatchDto:
    player1_name: str
    player2_name: str
    winner_name: str