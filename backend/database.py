from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from backend.config import get_settings

settings = get_settings()

_is_supabase = "supabase.co" in settings.database_url or "pooler.supabase.com" in settings.database_url
_is_pooler = "pooler.supabase.com" in settings.database_url
_connect_args = {}
if _is_supabase:
    _connect_args["ssl"] = "require"
if _is_pooler:
    # PgBouncer (transaction mode) doesn't support prepared statements
    _connect_args["statement_cache_size"] = 0
engine = create_async_engine(settings.database_url, echo=False, connect_args=_connect_args)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
