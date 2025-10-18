import os
from logging.config import fileConfig
from pathlib import Path

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from urllib.parse import quote_plus
from dotenv import load_dotenv
from src.database.models.match import Match # noqa
from src.database.models.player import Player # noqa
from tennis_match_scoreboard.src.database.db import Base
from alembic import context

config = context.config

env_path = Path(__file__).resolve().parents[2] / '.env'
load_dotenv(dotenv_path=env_path)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

user = os.getenv("USERNAME_DB", "")
pwd = os.getenv("PASSWORD_DB", "")
host = os.getenv("DB_HOST", "localhost")
name = os.getenv("DB_NAME", "")
driver = os.getenv("DB_DRIVER", "mysql+pymysql")
pwd_enc = quote_plus(pwd) if pwd else ""
database_url = f"{driver}://{user}:{pwd_enc}@{host}/{name}"

config.set_main_option("sqlalchemy.url", database_url)

target_metadata = Base.metadata



def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
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
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
