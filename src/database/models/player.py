from src.database.db import Base
from sqlalchemy.orm import mapped_column
from sqlalchemy import Text
from sqlalchemy.orm import Mapped

class Player(Base):
    __tablename__ = "players_table"
    name: Mapped[str] = mapped_column(Text, index=True)