from sqlalchemy.orm import Query
import math
from tennis_match_scoreboard.src.dto.match_dto import MatchDto
from tennis_match_scoreboard.src.dto.page_content_dto import PageContentDto


class PaginationService:
    def __init__(self, page_size: int = 3):
        self.page_size = page_size

    def paginate(self, query: Query, page: int) -> PageContentDto:
        total_items = query.count()
        total_pages = math.ceil(total_items / self.page_size) if total_items > 0 else 1
        normalized_page = max(1, min(page, total_pages))
        offset = (normalized_page - 1) * self.page_size
        items = query.offset(offset).limit(self.page_size).all()

        matches_dto = [
            MatchDto(match.player1.name, match.player2.name, match.winner_player.name)
            for match in items
        ]
        return PageContentDto(matches_dto, total_items, total_pages, normalized_page)

