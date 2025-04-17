from app.config import Config
from app.container import Container
from contextlib import asynccontextmanager
from inspect import isawaitable
from os.path import exists
from dotenv import load_dotenv
from os import getenv


@asynccontextmanager
async def bootstrap():
    container = Container()
    if exists(".env"):
        load_dotenv(dotenv_path=".env", override=True)
    config = Config(
        version="0.1.0",
        ocr_space_api_key=getenv("OCR_SPACE_API_KEY"),
        sqlite_db_path=getenv("SQLITE_DB_PATH"),
    )
    container.config.from_dict(config.model_dump())
    container.wire(
        packages=[
            "app.modules.text_ripping.presentation.cli",
            "app.infrastructure.schemas.general",
        ]
    )
    if isawaitable(awaitable := container.init_resources()):
        await awaitable
    yield container
    if isawaitable(awaitable := container.shutdown_resources()):
        await awaitable
