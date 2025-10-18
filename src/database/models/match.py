from src.database.db import Base
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped


class Match(Base):
    __tablename__ = "matches_table"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    uuid: Mapped[str] = mapped_column(String(36), unique=True)
    player1_id: Mapped[int] = mapped_column(Integer, ForeignKey("players_table.id"))
    player2_id: Mapped[int] = mapped_column(Integer, ForeignKey("players_table.id"))
    winner: Mapped[int] = mapped_column(Integer, ForeignKey("players_table.id"))
    score: Mapped[str] = mapped_column(String(250))

    player1 = relationship('Player', foreign_keys=[player1_id])
    player2 = relationship('Player', foreign_keys=[player2_id])
    winner_player = relationship('Player', foreign_keys=[winner])
