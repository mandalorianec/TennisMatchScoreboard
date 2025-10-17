from tennis_match_scoreboard.src.dto.request_dto import RequestDTO
from tennis_match_scoreboard.src.exceptions.own_exceptions import UnsupportedMethodException


class Controller:
    def handle_get(self, request_dto: RequestDTO):
        raise UnsupportedMethodException("Метод GET не поддерживается для этого запроса")

    def handle_post(self, request_dto: RequestDTO):
        raise UnsupportedMethodException("Метод POST не поддерживается для этого запроса")
