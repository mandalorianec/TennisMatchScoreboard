from src.controllers.controller import Controller
from src.dto.request_dto import RequestDTO
from src.dto.response_dto import ResponseDto
from src.exceptions.own_exceptions import ValidationException
from src.service.ongoing_match_service import going_match_service
from src.utils.validator import Validator


class NewMatchController(Controller):
    def __init__(self, render, players_dao):
        self.render = render
        self.players_dao = players_dao

    def handle_get(self, request_dto: RequestDTO) -> ResponseDto:
        rendered_html = self.render.render_template("new-match.html", {})
        return ResponseDto('200 OK', [('Content-Type', 'text/html')], rendered_html)

    def handle_post(self, request_dto: RequestDTO) -> ResponseDto:
        try:
            player1_name = self._get_validated_player_name(request_dto.body_params["player1"][0])
            player2_name = self._get_validated_player_name(request_dto.body_params["player2"][0])
        except KeyError:
            return self._handle_exception('400 Bad request', "Укажите имя игрока")
        except ValidationException as e:
            return self._handle_exception(e.error_code, e.error_message)
        if player1_name == player2_name:
            return self._handle_exception('400 Bad request', "Имена игроков должны различаться")

        # if not dao.is_player_exist(player1_name):
        #     dao.add_new_player(player1_name)
        # if not dao.is_player_exist(player2_name):
        #     dao.add_new_player(player2_name)

        # player1_id, player2_id = self._get_players_id(player1_name, player2_name)
        # добавление локально
        match_uuid = going_match_service.add_match_local(self.players_dao, player1_name, player2_name)

        redirect_link = f"/match-score?uuid={match_uuid}"

        # тут редирект на /match-score?uuid=$match_uuid
        return ResponseDto('302 OK', [('Location', redirect_link)], '')

    @staticmethod
    def _get_validated_player_name(player_name: str) -> str:
        Validator.validate_player_name(player_name)
        return player_name.strip().lower()



    def _handle_exception(self, error_code: str, error_message: str):
        rendered_html = self.render.render_template("new-match.html", {"error": error_message})
        return ResponseDto(error_code, [('Content-Type', 'text/html')], rendered_html)
