from dependency_injector.containers import DeclarativeContainer
from dependency_injector import providers

from src.controllers.index_controller import IndexController
from src.controllers.match_score_controller import MatchScoreController
from src.controllers.matches_controller import MatchesController
from src.controllers.new_match_controller import NewMatchController
from src.dao.matches_dao import MatchesDao
from src.dao.players_dao import PlayersDao
from src.utils.render import Render


class Container(DeclarativeContainer):
    players_dao = providers.Singleton(PlayersDao)
    matches_dao = providers.Singleton(MatchesDao)
    render = providers.Singleton(Render)

    index_contoller = providers.Factory(
        IndexController,
        render=render
    )

    match_score_controller = providers.Factory(
        MatchScoreController,
        render=render,
        matches_dao=matches_dao,
    )

    matches_controller = providers.Factory(
        MatchesController,
        render=render,
        matches_dao=matches_dao,
    )

    new_match_controller = providers.Factory(
        NewMatchController,
        render=render,
        players_dao=players_dao,
    )
