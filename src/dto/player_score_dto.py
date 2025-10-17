from dataclasses import dataclass


@dataclass
class PlayerScoreDto:
    sets: int = 0
    games: int = 0
    points: int = 0