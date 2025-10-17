from typing import Optional

from tennis_match_scoreboard.src.dto.player_score_dto import PlayerScoreDto
from tennis_match_scoreboard.src.dto.score_dto import ScoreDto
from tennis_match_scoreboard.src.service.tennis_set import Set


class MatchCounterService:
    def __init__(self, player1: PlayerScoreDto, player2: PlayerScoreDto):
        self.player1 = player1
        self.player2 = player2
        self.current_set = Set(self.player1, self.player2)

    def add_point_to(self, player_number: int) -> Optional[int]:
        winner_set_number = self.current_set.add_point_to(player_number)
        if winner_set_number:
            self._on_set_won(player_number)

            match_winner_number = self._get_number_match_win()
            if match_winner_number:
                return match_winner_number
        return None

    def _on_set_won(self, player_number: int) -> None:
        if player_number == 1:
            self.player1.sets += 1
        else:
            self.player2.sets += 1
        self._reset_games()
        self.current_set = Set(self.player1, self.player2)

    def _reset_games(self) -> None:
        self.player1.games = 0
        self.player2.games = 0

    def _get_number_match_win(self) -> Optional[int]:
        if self.player1.sets >= 2:
            return 1
        if self.player2.sets >= 2:
            return 2
        return None

    def get_score(self) -> ScoreDto:
        score = ScoreDto(self.player1, self.player2)
        return score
