from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()
user = os.getenv("USERNAME_DB")
password = os.getenv("PASSWORD_DB")

mysql_database = f"mysql+pymysql://{user}:{password}@localhost/db"

engine = create_engine(mysql_database, echo=False, pool_pre_ping=True, pool_size=3600)

session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase): pass


Base.metadata.create_all(bind=engine)
