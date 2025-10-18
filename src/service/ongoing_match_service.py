import uuid
from src.dto.going_match_dto import GoingMatchDto
from src.dto.score_dto import ScoreDto
from src.dto.player_score_dto import PlayerScoreDto
from src.dao.matches_dao import MatchesDao


class OngoingMatchService:
    def __init__(self):
        self.going_matchs = {}

    def add_match_local(self, player1_id: int, player2_id: int) -> str:
        random_uuid = str(uuid.uuid4())
        score = ScoreDto(PlayerScoreDto(), PlayerScoreDto())
        new_match = GoingMatchDto(player1_id, player2_id, random_uuid, score)
        self.going_matchs[random_uuid] = new_match
        return random_uuid

    def get_local_match_by(self, uuid_match: str) -> GoingMatchDto:
        return self.going_matchs[uuid_match]

    def update_match_score(self, uuid_match: str, new_score: ScoreDto) -> None:
        self.going_matchs[uuid_match].score = new_score

    def finish_match(self, uuid_match: str, winner_id: int) -> None:
        dao = MatchesDao()
        dao.add_finished_match(self.going_matchs[uuid_match], winner_id)
        self.going_matchs.pop(uuid_match)


going_match_service = OngoingMatchService()
