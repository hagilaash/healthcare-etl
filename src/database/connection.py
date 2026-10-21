from sqlalchemy import URL, create_engine, text
from sqlalchemy.engine import Engine

from config.settings import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
)


def get_database_url() -> URL:
    """Build the PostgreSQL connection URL safely."""

    if not DB_USER or not DB_PASSWORD:
        raise ValueError(
            "DB_USER and DB_PASSWORD must be configured in the .env file."
        )

    return URL.create(
        drivername="postgresql+psycopg",
        username=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
    )


def get_engine() -> Engine:
    """Create a SQLAlchemy engine for PostgreSQL."""

    return create_engine(
        get_database_url(),
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
    )


def test_database_connection() -> bool:
    """Check whether PostgreSQL is reachable."""

    engine = get_engine()

    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1")).scalar_one()
            return result == 1
    finally:
        engine.dispose()
