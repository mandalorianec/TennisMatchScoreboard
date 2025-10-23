from src.controllers.controller import Controller
from src.dto.request_dto import RequestDTO
from src.dto.response_dto import ResponseDto


class IndexController(Controller):
    def __init__(self, render):
        self.render = render

    def handle_get(self, request_dto: RequestDTO) -> ResponseDto:
        rendered_html = self.render.render_template("index.html", {})
        return ResponseDto('200 OK', [('Content-Type', 'text/html')], rendered_html)
