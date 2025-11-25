from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from collections.abc import AsyncGenerator
from sqlalchemy import event


from app.config import settings


DATABASE_URL_asyncpg = settings.DATABASE_URL_asyncpg

# async_engine  = create_async_engine(DATABASE_URL_asyncpg) # вариант Postgresql
async_engine = create_async_engine(
    DATABASE_URL_asyncpg,
    echo=False,
    connect_args={"check_same_thread": False}  # вариант SQLite
)
@event.listens_for(async_engine.sync_engine, "connect")
def enable_sqlite_fk(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

async_session_factory  = async_sessionmaker(autocommit=False, autoflush=False, bind=async_engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_session() -> AsyncGenerator:
    async with async_session_factory() as session:
        yield session