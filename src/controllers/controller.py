from src.dao.matches_dao import MatchesDao
from src.dao.players_dao import PlayersDao
from src.dto.request_dto import RequestDTO
from src.exceptions.own_exceptions import UnsupportedMethodException


class Controller:
    def handle_get(self, request_dto: RequestDTO):
        raise UnsupportedMethodException("Метод GET не поддерживается для этого запроса")

    def handle_post(self, request_dto: RequestDTO):
        raise UnsupportedMethodException("Метод POST не поддерживается для этого запроса")
