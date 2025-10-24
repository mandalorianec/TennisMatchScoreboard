from src.controllers.controller import Controller
from src.dto.match_dto import MatchDto
from src.dto.page_content_dto import PageContentDto
from src.dto.request_dto import RequestDTO
from src.dto.response_dto import ResponseDto


class MatchesController(Controller):
    def __init__(self, render, matches_dao):
        self.render = render
        self.matches_dao = matches_dao

    def handle_get(self, request_dto: RequestDTO) -> ResponseDto:
        page = int(request_dto.query_params.get("page", ["1"])[0])  # запрашиваемая страница
        filter_by_player_name = request_dto.query_params.get("filter_by_player_name", " ")[0].strip().lower()
        page_content = self.matches_dao.get_matches(page=page, player_name=filter_by_player_name)
        if page_content.current_page != page:  # редирект на последнюю страницу
            return ResponseDto('302 Found',
                               [('Location',
                                 f'/matches?page={page_content.current_page}&filter_by_player_name={filter_by_player_name}')],
                               '')
        context = self.get_context(page_content, filter_by_player_name)
        rendered_html = self.render.render_template("matches.html", context)
        return ResponseDto('200 OK', [('Content-Type', 'text/html')], rendered_html)

    @staticmethod
    def get_context(page_content: PageContentDto, filter_name: str) -> dict[str, str | int | list[MatchDto]]:
        context = {
            "matches": page_content.matches,
            "total_items": page_content.total_items,
            "total_pages": page_content.total_pages,
            "current_page": page_content.current_page,
            "name": filter_name
        }
        return context
