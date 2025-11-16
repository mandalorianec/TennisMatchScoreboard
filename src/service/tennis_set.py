from typing import Optional

from src.dto.player_score_dto import PlayerScoreDto
from src.service.tennis_game import Game
from src.service.tie_break import TieBreak


class TennisSet:
    def __init__(self, player1: PlayerScoreDto, player2: PlayerScoreDto):
        self.player1 = player1
        self.player2 = player2
        self.current_game = Game(self.player1, self.player2)
        self.tie_break = TieBreak(self.player1, self.player2)

    def add_point_to(self, player_number: int) -> Optional[int]:
        if self.player1.games == self.player2.games and self.player2.games == 6:
            tie_break_winner = self.tie_break.add_point_to(player_number)
            return tie_break_winner
        game_winner_number = self.current_game.add_point_to(player_number)
        if game_winner_number:
            self._on_game_won(player_number)

            winner_set_number = self._get_number_set_win()
            if winner_set_number:
                return winner_set_number

        return None

    def _on_game_won(self, player_number: int) -> None:
        if player_number == 1:
            self.player1.games += 1
        else:
            self.player2.games += 1
        self.current_game = Game(self.player1, self.player2)

    def _get_number_set_win(self) -> Optional[int]:
        if self.player1.games >= 6 and (self.player1.games - self.player2.games) >= 2:
            return 1
        if self.player2.games >= 6 and (self.player2.games - self.player1.games) >= 2:
            return 2
        return None
