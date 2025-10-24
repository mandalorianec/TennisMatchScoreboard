import json
from dataclasses import asdict

from sqlalchemy.orm import Query
from src.dto.page_content_dto import PageContentDto
from src.service.pagination_service import PaginationService
from src.service.ongoing_match_service import GoingMatchDto
from sqlalchemy.orm import joinedload
from sqlalchemy import or_
from src.database.models.player import Player
from src.database.models.match import Match
from src.database.session import get_db


class MatchesDao:
    @staticmethod
    def add_finished_match(match: GoingMatchDto, winner_id: int) -> None:
        with get_db() as db:
            finished_match = Match(
                uuid=match.uuid,
                player1_id=match.player1.id,
                player2_id=match.player2.id,
                winner=winner_id,
                score=json.dumps(asdict(match.score))
            )
            db.add(finished_match)

    def get_matches(self, page: int = 1, player_name: str | None = None) -> PageContentDto:
        query = self._build_matches_query(player_name)
        query = query.order_by(Match.id.desc())

        paginator = PaginationService()
        return paginator.paginate(query, page)

    @staticmethod
    def _build_matches_query(player_name: str) -> Query:
        with get_db() as db:
            query = db.query(Match).options(
                joinedload(Match.player1),
                joinedload(Match.player2),
            )
            if player_name:
                search_query = f"%{player_name}%"
                query = query.filter(
                    or_(
                        Match.player1.has(Player.name.ilike(search_query)),
                        Match.player2.has(Player.name.ilike(search_query)),
                    )
                )
            return query
