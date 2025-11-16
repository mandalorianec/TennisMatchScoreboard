from src.database.db import Base
from sqlalchemy.orm import mapped_column
from sqlalchemy import String
from sqlalchemy.orm import Mapped

class Player(Base):
    __tablename__ = "players_table"
    name: Mapped[str] = mapped_column(String(30), index=True)