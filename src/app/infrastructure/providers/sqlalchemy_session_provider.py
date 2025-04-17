from app.infrastructure.schemas.general.base import Base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker


async def provide_sqlalchemy_session(sqlite_db_path: str):
    engine = create_async_engine(sqlite_db_path, echo=False)
    async with engine.begin() as transaction:
        await transaction.run_sync(Base.metadata.create_all)
    make_session = async_sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )
    yield make_session
    await engine.dispose()
