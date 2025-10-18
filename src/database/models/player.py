from src.database.db import Base
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped

class Player(Base):
    __tablename__ = "players_table"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30), index=True)