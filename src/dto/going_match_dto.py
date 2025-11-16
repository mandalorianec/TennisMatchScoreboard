from dataclasses import dataclass
from src.dto.player_dto import PlayerDto
from src.dto.score_dto import ScoreDto
from uuid import UUID


@dataclass
class GoingMatchDto:
    player1: PlayerDto
    player2: PlayerDto
    uuid: UUID
    score: ScoreDto
