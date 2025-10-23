from dataclasses import dataclass
from src.dto.player_dto import PlayerDto
from src.dto.score_dto import ScoreDto


@dataclass
class GoingMatchDto:
    # player1_id: int
    # player2_id: int
    # player1_name: str
    # player2_name: str
    player1: PlayerDto
    player2: PlayerDto
    uuid: str
    score: ScoreDto
