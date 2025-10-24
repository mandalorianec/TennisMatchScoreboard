import os
import sys
from logging.config import fileConfig
from pathlib import Path
from dotenv import load_dotenv

from alembic import context
from sqlalchemy import engine_from_config, pool

# models must be imported so target_metadata is populated
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.database.models.match import Match  # noqa: F401
from src.database.models.player import Player  # noqa: F401
from src.database.db import Base  # noqa: F401

config = context.config

# load .env from project root
env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

user = os.getenv("USERNAME_DB", "")
pwd = os.getenv("PASSWORD_DB", "")
host = os.getenv("DB_HOST", "localhost")
name = os.getenv("DB_NAME", "")
driver = os.getenv("DB_DRIVER", "mysql+pymysql")

database_url = f"{driver}://{user}:{pwd}@{host}/{name}"

config.set_main_option("sqlalchemy.url", database_url)
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
