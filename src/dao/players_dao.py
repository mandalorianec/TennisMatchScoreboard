from typing import Optional

from sqlalchemy import func
from src.database.session import get_db
from src.database.models.player import Player


class PlayersDao:
    def get_player_id_by(self, player_name: str) -> Optional[int]:
        with get_db() as db:
            player = db.query(Player).filter(func.lower(Player.name) == player_name.lower()).first()
            if player:
                return player.id
            return None

    def is_player_exist(self, player_name: str) -> bool:
        if self.get_player_id_by(player_name):
            return True
        return False

    def add_new_player(self, player_name: str) -> None:
        with get_db() as db:
            new_player = Player(name=player_name)
            db.add(new_player)

    def get_player_name_by(self, player_id: int) -> str:
        with get_db() as db:
            player = db.query(Player).filter(Player.id == player_id).first()
            return str(player.name)
