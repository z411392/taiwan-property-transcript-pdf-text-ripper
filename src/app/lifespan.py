from contextlib import asynccontextmanager
from os.path import exists
from dotenv import load_dotenv
from os import getenv
from injector import Injector, InstanceProvider
from app.adapters.http.ocr_space import OCRSpace
from app.infrastructure.hashers.bytes_hasher import BytesHasher
from app.infrastructure.schemas.general.base import Base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker


@asynccontextmanager
async def lifespan():
    if exists(".env"):
        load_dotenv(dotenv_path=".env", override=True)
    engine = create_async_engine(getenv("SQLITE_DB_PATH"), echo=False)
    async with engine.begin() as transaction:
        await transaction.run_sync(Base.metadata.create_all)
    injector = Injector()
    injector.binder.bind(BytesHasher, to=InstanceProvider(BytesHasher()))
    injector.binder.bind(
        OCRSpace, to=InstanceProvider(OCRSpace(api_key=getenv("OCR_SPACE_API_KEY")))
    )
    injector.binder.bind(
        async_sessionmaker[AsyncSession],
        to=InstanceProvider(
            async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
        ),
    )
    yield injector
    await engine.dispose()
