from dataclasses import dataclass
from src.dto.score_dto import ScoreDto


@dataclass
class FormattedPlayerScoreDto:
    sets: int = 0
    games: int = 0
    points: str = "0"


@dataclass
class FormattedScoreDto:
    player1: FormattedPlayerScoreDto
    player2: FormattedPlayerScoreDto


class ScoreFormatter:
    _POINT_MAP = {0: '0', 1: '15', 2: '30', 3: '40'}

    def format(self, score: ScoreDto, is_tie_break: bool) -> FormattedScoreDto:
        pl1_score = score.player1
        pl2_score = score.player2
        if is_tie_break:
            formatted_score = FormattedScoreDto(
                player1=FormattedPlayerScoreDto(pl1_score.sets, pl1_score.games, str(pl1_score.points)),
                player2=FormattedPlayerScoreDto(pl2_score.sets, pl2_score.games, str(pl2_score.points))
            )
            return formatted_score

        if pl1_score.points >= 3 and pl2_score.points >= 3:
            if pl1_score.points == pl2_score.points:
                pl1_disp_points = pl2_disp_points = "Deuce"
            elif pl1_score.points - pl2_score.points == 1:
                pl1_disp_points = "Adv"
                pl2_disp_points = "40"
            elif pl2_score.points - pl1_score.points == 1:
                pl2_disp_points = "Adv"
                pl1_disp_points = "40"
            else:
                pl1_disp_points = self._POINT_MAP.get(min(pl1_score.points, 3), '40')
                pl2_disp_points = self._POINT_MAP.get(min(pl2_score.points, 3), '40')
        else:
            pl1_disp_points = self._POINT_MAP.get(pl1_score.points, "40")
            pl2_disp_points = self._POINT_MAP.get(pl2_score.points, "40")

        formatted_score = FormattedScoreDto(
            player1=FormattedPlayerScoreDto(pl1_score.sets, pl1_score.games, pl1_disp_points),
            player2=FormattedPlayerScoreDto(pl2_score.sets, pl2_score.games, pl2_disp_points)
        )
        return formatted_score
