from src.controllers.match_score_controller import MatchScoreController
from src.controllers.new_match_controller import NewMatchController
from src.controllers.index_controller import IndexController
from src.controllers.matches_controller import MatchesController
from src.dto.response_dto import ResponseDto
from src.exceptions.own_exceptions import ControllerNotFoundException, UnsupportedMethodException


class Router:
    _routers = {
        "/": IndexController,
        "/new-match": NewMatchController,
        "/match-score": MatchScoreController,
        "/matches": MatchesController,
    }

    @staticmethod
    def find_controller(path: str):
        handler = Router._routers.get(path)
        if not handler:
            raise ControllerNotFoundException(f"Страница {path} не найдена")
        return handler

    @staticmethod
    def perform(controller, request_dto) -> ResponseDto:
        method = request_dto.method.upper()
        if method == 'GET':
            return controller.handle_get(request_dto)
        if method == 'POST':
            return controller.handle_post(request_dto)
        if method == 'OPTIONS':
            return controller.hadle_options(request_dto)
        raise UnsupportedMethodException(f"Метод {method} не поддерживается")