import unittest

from tennis_match_scoreboard.src.dto.score_dto import ScoreDto
from tennis_match_scoreboard.src.service.match_score_service import MatchCounterService
from tennis_match_scoreboard.src.dto.player_score_dto import PlayerScoreDto
from src.utils.score_formatter import ScoreFormatter


# запуск \TennisMatchScoreboard> python -m unittest discover -s tennis_match_scoreboard\tests -p "test_*.py" -v


def _is_tie_break(player1_score: PlayerScoreDto, player2_score: PlayerScoreDto):
    return player1_score.games == player2_score.games == 6


class TestCountPoints(unittest.TestCase):
    def setUp(self):
        self.formatter = ScoreFormatter()

    def _get_formatted_score_points(self, score: ScoreDto) -> tuple[str, str]:
        formatted_score = self.formatter.format(score, _is_tie_break(score.player1, score.player2))
        return formatted_score.player1.points, formatted_score.player2.points

    def test_tie_break(self):
        """
        Если игрок 1 выигрывает очко при счёте 40-40, гейм не заканчивается
        """
        player_score1 = PlayerScoreDto(0, 0, 3)
        player_score2 = PlayerScoreDto(0, 0, 3)
        counter = MatchCounterService(player_score1, player_score2)
        pred_games = counter.get_score().player1.games
        counter.add_point_to(1)
        self.assertEqual(counter.get_score().player1.games, pred_games)

    def test_final_point_in_game(self):
        """
        Если игрок 1 выигрывает очко при счёте 40-0, то он выигрывает и гейм
        """
        player_score1 = PlayerScoreDto(0, 0, 3)
        player_score2 = PlayerScoreDto(0, 0, 0)
        counter = MatchCounterService(player_score1, player_score2)
        pred_games = counter.get_score().player1.games
        counter.add_point_to(1)
        self.assertEqual(counter.get_score().player1.games, pred_games + 1)

    def test_start_tie_break(self):
        """
        При счёте 6-6 начинается тайбрейк вместо обычного гейма
        """
        player_score1 = PlayerScoreDto(0, 6, 0)
        player_score2 = PlayerScoreDto(0, 6, 0)
        counter = MatchCounterService(player_score1, player_score2)
        counter.add_point_to(1)
        counter.add_point_to(1)
        counter.add_point_to(1)
        counter.add_point_to(1)
        counter.add_point_to(1)
        self.assertEqual(counter.get_score().player1.points, 5)

    def test_3_points_both(self):
        """
        При счёте 40-40 должно отображаться "Deuce" для обоих
        """
        player_score1 = PlayerScoreDto(0, 0, 3)
        player_score2 = PlayerScoreDto(0, 0, 3)
        counter = MatchCounterService(player_score1, player_score2)
        score = counter.get_score()

        formatter_score = self.formatter.format(score, _is_tie_break(player_score1, player_score2))

        self.assertEqual((formatter_score.player1.points, formatter_score.player2.points), ("Deuce", "Deuce"))

    def test_player1_advantage(self):
        """
        Проверить, когда один игрок имеет преимущество: 4-3 → "Adv"-"40"
        """
        player_score1 = PlayerScoreDto(0, 0, 4)
        player_score2 = PlayerScoreDto(0, 0, 3)
        counter = MatchCounterService(player_score1, player_score2)

        score = counter.get_score()

        formatter_score = self.formatter.format(score, _is_tie_break(player_score1, player_score2))
        self.assertEqual((formatter_score.player1.points, str(formatter_score.player2.points)), ("Adv", "40"))

    def test_player2_advantage(self):
        """
        Проверить обратную ситуацию: 3-4 → "40"-"Adv"
        """
        player_score1 = PlayerScoreDto(0, 0, 3)
        player_score2 = PlayerScoreDto(0, 0, 4)
        counter = MatchCounterService(player_score1, player_score2)

        score = counter.get_score()

        formatter_score = self.formatter.format(score, _is_tie_break(player_score1, player_score2))
        self.assertEqual((formatter_score.player1.points, str(formatter_score.player2.points)), ("40", "Adv"))

    def test_border_count(self):
        """
        Проверить переход от 40-30 к Advantage и обратно к Deuce
        """
        player_score1 = PlayerScoreDto(0, 0, 2)
        player_score2 = PlayerScoreDto(0, 0, 2)
        counter = MatchCounterService(player_score1, player_score2)

        counter.add_point_to(1)  # 40-30
        counter.add_point_to(2)
        counter.add_point_to(2)  # 40-Adv

        score = counter.get_score()
        formatted_points = self._get_formatted_score_points(score)

        self.assertEqual(formatted_points, ("40", "Adv"))
        counter.add_point_to(1)

        score = counter.get_score()
        formatted_points = self._get_formatted_score_points(score)

        self.assertEqual(formatted_points, ("Deuce", "Deuce"))

    def test_high_scores_non_tiebreak(self):
        """Проверка счета больше 3 очков при разнице >1"""
        score = ScoreDto(
            player1=PlayerScoreDto(0, 0, 5),  # 5 очков
            player2=PlayerScoreDto(0, 0, 2)  # 2 очка
        )
        p1_disp, p2_disp = self._get_formatted_score_points(score)
        self.assertEqual((p1_disp, p2_disp), ("40", "30"))


if __name__ == '__main__':
    unittest.main()
