from src.dto.response_dto import ResponseDto
from src.exceptions.own_exceptions import ControllerNotFoundException, UnsupportedMethodException
from src.utils.container import Container


class Router:
    def __init__(self, container: Container):
        self.container = container
        self._routes = {
            "/": self.container.IndexController,
            "/new-match": self.container.NewMatchController,
            "/match-score": self.container.MatchScoreController,
            "/matches": self.container.MatchesController,
        }

    def find_controller(self, path: str):
        handler = self._routes.get(path)
        if not handler:
            raise ControllerNotFoundException(f"Страница {path} не найдена")
        return handler()

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
