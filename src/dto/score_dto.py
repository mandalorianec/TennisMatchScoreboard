from dataclasses import dataclass
from src.dto.player_score_dto import PlayerScoreDto

@dataclass
class ScoreDto:
    player1: PlayerScoreDto
    player2: PlayerScoreDto
