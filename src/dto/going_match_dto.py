from dataclasses import dataclass

from tennis_match_scoreboard.src.dto.score_dto import ScoreDto


@dataclass
class GoingMatchDto:
    player1_id: int
    player2_id: int
    uuid: str
    score: ScoreDto
