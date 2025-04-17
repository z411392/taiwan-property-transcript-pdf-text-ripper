import pytest
from app.bootstrap import bootstrap
from app.container import Container
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from app.adapters.sqlite.ocr_result_repository import OCRResultRepository
from os import getenv


@pytest.mark.skipif(getenv("GITHUB_ACTIONS") != "true", reason="")
class TestSQLite:
    @pytest.fixture
    async def container(self):
        async with bootstrap() as container:
            yield container

    @pytest.fixture
    async def make_session(self, container: Container):
        make_session = await container.make_session()
        return make_session

    @pytest.mark.describe("要能夠用 SQLite 儲存 OCR 結果")
    async def test_sqlite_save_ocr_result(
        self,
        make_session: async_sessionmaker[AsyncSession],
        sample_image_hash: str,
        sample_ocr_result: str,
    ):
        try:
            async with make_session() as session:
                ocr_result_repository = OCRResultRepository(session=session)
                await ocr_result_repository.save(sample_image_hash, sample_ocr_result)
        except Exception as exception:
            pytest.fail(f"儲存 OCR 結果失敗: {exception}")

    @pytest.mark.describe("要能夠用 SQLite 讀取儲存的 OCR 結果")
    async def test_sqlite_load_ocr_result(
        self,
        make_session: async_sessionmaker[AsyncSession],
        sample_image_hash: str,
        sample_ocr_result: str,
    ):
        async with make_session() as session:
            ocr_result_repository = OCRResultRepository(session=session)
            ocr_result = await ocr_result_repository.load(sample_image_hash)
            assert ocr_result == sample_ocr_result
