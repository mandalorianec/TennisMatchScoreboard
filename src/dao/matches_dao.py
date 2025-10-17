import json
from sqlalchemy.orm import Query
from tennis_match_scoreboard.src.dto.page_content_dto import PageContentDto
from tennis_match_scoreboard.src.dto.score_dto import ScoreDto
from tennis_match_scoreboard.src.service.pagination_service import PaginationService
from tennis_match_scoreboard.src.service.ongoing_match_service import GoingMatchDto
from sqlalchemy.orm import joinedload
from sqlalchemy import or_
from tennis_match_scoreboard.src.database.models.player import Player
from tennis_match_scoreboard.src.database.models.match import Match
from src.utils.score_formatter import ScoreFormatter
from tennis_match_scoreboard.src.database.session import get_db


class MatchesDao:
    def add_finished_match(self, match: GoingMatchDto, winner_id: int) -> None:
        with get_db() as db:
            formatted_score = self._format_score(match.score)
            finished_match = Match(
                uuid=match.uuid,
                player1_id=match.player1_id,
                player2_id=match.player2_id,
                winner=winner_id,
                score=json.dumps(formatted_score)
            )
            db.add(finished_match)

    def get_matches(self, page: int = 1, player_name: str | None = None) -> PageContentDto:
        query = self._build_matches_query(player_name)
        query = query.order_by(Match.id.desc())

        paginator = PaginationService()
        return paginator.paginate(query, page)

    @staticmethod
    def _format_score(score: ScoreDto) -> dict:
        formatter = ScoreFormatter()
        formatted = formatter.format(score, score.player1.games == score.player2.games == 6)

        return {
            "player1": {
                "sets": formatted.player1.sets,
                "games": formatted.player1.games,
                "points": formatted.player1.points
            },
            "player2": {
                "sets": formatted.player2.sets,
                "games": formatted.player2.games,
                "points": formatted.player2.points,
            }
        }

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
