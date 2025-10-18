from typing import Optional

from src.dto.player_score_dto import PlayerScoreDto


class Game:
    def __init__(self, player1: PlayerScoreDto, player2: PlayerScoreDto):
        self.player1 = player1
        self.player2 = player2
        self.min_points_to_win = 4
        self.min_difference = 2

    def add_point_to(self, player_number: int) -> Optional[int]:
        if player_number == 1:
            self.player1.points += 1
        else:
            self.player2.points += 1
        game_winner = self._get_number_game_win()
        if game_winner:
            self._reset_points()
            return game_winner
        return None

    def _get_number_game_win(self) -> Optional[int]:
        if self.player1.points >= self.min_points_to_win and (
                self.player1.points - self.player2.points) >= self.min_difference:
            return 1
        if self.player2.points >= self.min_points_to_win and (
                self.player2.points - self.player1.points) >= self.min_difference:
            return 2
        return None

    def _reset_points(self):
        self.player1.points = 0
        self.player2.points = 0
