from src.controllers.controller import Controller
from src.dao.players_dao import PlayersDao
from src.dto.request_dto import RequestDTO
from src.dto.response_dto import ResponseDto
from src.utils.render import Render
from src.service.ongoing_match_service import going_match_service
from src.service.match_score_service import MatchCounterService
from src.utils.score_formatter import ScoreFormatter, FormattedScoreDto


class MatchScoreController(Controller):
    def __init__(self):
        self.render = Render()

    def handle_get(self, request_dto: RequestDTO) -> ResponseDto:
        dao = PlayersDao()
        uuid = request_dto.query_params.get("uuid", " ")[0]
        try:
            match = going_match_service.get_local_match_by(uuid)
        except KeyError:
            return self._handle_exception('400 Bad request', "Матч с таким uuid не существует или уже завершён")

        name1 = dao.get_player_name_by(match.player1_id)
        name2 = dao.get_player_name_by(match.player2_id)
        match_score = match.score
        formatter = ScoreFormatter()
        formatted_score = formatter.format(match_score, match_score.player1.games == match_score.player2.games == 6)
        context = self.get_context(uuid, name1, name2, formatted_score)

        rendered_html = self.render.render_template("match-score.html", context)
        return ResponseDto('200 OK', [('Content-Type', 'text/html')], rendered_html)

    def handle_post(self, request_dto: RequestDTO) -> ResponseDto:
        uuid = request_dto.body_params.get("uuid", " ")[0]
        player_number = int(request_dto.body_params.get("player", " ")[0])
        try:
            match = going_match_service.get_local_match_by(uuid)
        except KeyError:
            return ResponseDto('303 See Other', [('Location', f'/matches')], '')
        match_score = match.score
        match_service = MatchCounterService(match_score.player1, match_score.player2)
        match_winner = match_service.add_point_to(player_number)

        score = match_service.get_score()

        going_match_service.update_match_score(uuid, score)
        if match_winner:
            if match_winner == 1:
                match_winner_id = match.player1_id
            else:
                match_winner_id = match.player2_id
            going_match_service.finish_match(uuid, match_winner_id)
            return ResponseDto('303 See Other', [('Location', f'/matches')], '')
        return ResponseDto('303 See Other', [('Location', f'/match-score?uuid={uuid}')], '')

    @staticmethod
    def get_context(uuid: str, name1: str, name2: str, score: FormattedScoreDto) -> dict[str, str | int]:
        context = {
            "uuid": uuid,
            "name1": name1,
            "name2": name2,
            "sets1": score.player1.sets,
            "sets2": score.player2.sets,
            "games1": score.player1.games,
            "games2": score.player2.games,
            "points1": score.player1.points,
            "points2": score.player2.points,
        }
        return context

    def _handle_exception(self, error_code: str, error_message: str):
        rendered_html = self.render.render_template("error.html", {"error_code": error_code,
                                                                   "error_message": error_message})
        return ResponseDto(error_code, [('Content-Type', 'text/html')], rendered_html)
