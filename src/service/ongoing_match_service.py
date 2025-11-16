import uuid
from dataclasses import asdict

from src.dao.players_dao import PlayersDao
from src.dto.going_match_dto import GoingMatchDto
from src.dto.player_dto import PlayerDto
from src.dto.score_dto import ScoreDto
from src.dto.player_score_dto import PlayerScoreDto
from src.exceptions.own_exceptions import StringLimitException


class OngoingMatchService:
    def __init__(self):
        self.going_matchs = {}

    def add_match_local(self, players_dao: PlayersDao, player1_name: str, player2_name: str) -> str:
        if not players_dao.is_player_exist(player1_name):
            players_dao.add_new_player(player1_name)
        if not players_dao.is_player_exist(player2_name):
            players_dao.add_new_player(player2_name)

        player1_id, player2_id = self._get_players_id(players_dao, player1_name, player2_name)
        random_uuid = str(uuid.uuid4())
        score = ScoreDto(PlayerScoreDto(), PlayerScoreDto())

        new_match = GoingMatchDto(
            PlayerDto(player1_id, player1_name),
            PlayerDto(player2_id, player2_name),
            random_uuid,
            score
        )
        self.going_matchs[random_uuid] = new_match
        return random_uuid

    def get_local_match_by(self, uuid_match: str) -> GoingMatchDto:
        return self.going_matchs.get(uuid_match)

    def update_match_score(self, uuid_match: str, new_score: ScoreDto) -> None:
        self.going_matchs[uuid_match].score = new_score

    def finish_match(self, matches_dao, uuid_match: str, winner_id: int) -> None:
        if len(asdict(self.get_local_match_by(uuid_match).score)) > 250:
            raise StringLimitException("Превышена длина счёта")
        matches_dao.add_finished_match(self.going_matchs[uuid_match], winner_id)
        self.going_matchs.pop(uuid_match)

    @staticmethod
    def _get_players_id(dao: PlayersDao, player1_name: str, player2_name: str) -> tuple[int, int]:
        player1_id = dao.get_player_id_by(player1_name)
        player2_id = dao.get_player_id_by(player2_name)
        return player1_id, player2_id


going_match_service = OngoingMatchService()
