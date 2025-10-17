from tennis_match_scoreboard.src.dto.player_score_dto import PlayerScoreDto
from tennis_match_scoreboard.src.service.tennis_game import Game


class TieBreak(Game):
    def __init__(self, player1: PlayerScoreDto, player2: PlayerScoreDto):
        super().__init__(player1, player2)
        self.min_points_to_win = 7
