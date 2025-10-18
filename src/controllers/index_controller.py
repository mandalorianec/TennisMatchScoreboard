from src.controllers.controller import Controller
from src.dto.request_dto import RequestDTO
from src.dto.response_dto import ResponseDto
from src.utils.render import Render


class IndexController(Controller):
    def handle_get(self, request_dto: RequestDTO) -> ResponseDto:
        render = Render()
        rendered_html = render.render_template("index.html", {})
        return ResponseDto('200 OK', [('Content-Type', 'text/html')], rendered_html)
