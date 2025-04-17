import pytest
from app.bootstrap import bootstrap
from app.container import Container
from app.adapters.http.ocr_space import OCRSpace
from os import getenv


@pytest.mark.skipif(getenv("GITHUB_ACTIONS") != "true", reason="")
class TestOCRSpace:
    @pytest.fixture
    async def container(self):
        async with bootstrap() as container:
            yield container

    @pytest.fixture
    async def ocr_space(self, container: Container):
        ocr_space = container.ocr_space()
        return ocr_space

    @pytest.mark.describe("要能夠 ocr")
    async def test_ocr(
        self,
        sample_image: bytes,
        ocr_space: OCRSpace,
        sample_ocr_result: str,
    ):
        text = await ocr_space.ocr(sample_image)
        assert text == sample_ocr_result
