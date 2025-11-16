from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer
from src.config import user, password

mysql_database = f"mysql+pymysql://{user}:{password}@localhost/db"

engine = create_engine(mysql_database, echo=False, pool_pre_ping=True, pool_size=3600)

session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)



Base.metadata.create_all(bind=engine)
