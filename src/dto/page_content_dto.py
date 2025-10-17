from dataclasses import dataclass

from tennis_match_scoreboard.src.dto.match_dto import MatchDto


@dataclass
class PageContentDto:
    matches: list[MatchDto]
    total_items: int
    total_pages: int
    current_page: int
