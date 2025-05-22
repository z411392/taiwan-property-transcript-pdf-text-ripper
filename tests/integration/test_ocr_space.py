import pytest
from app.adapters.http.ocr_space import OCRSpace
from os import getenv
from app.lifespan import lifespan


@pytest.mark.skipif(getenv("GITHUB_ACTIONS") != "true", reason="")
class TestOCRSpace:
    @pytest.fixture
    async def ocr_space(self):
        async with lifespan() as injector:
            yield injector.get(OCRSpace)

    @pytest.mark.describe("要能夠 ocr")
    async def test_ocr(
        self,
        sample_image: bytes,
        ocr_space: OCRSpace,
        sample_ocr_result: str,
    ):
        text = await ocr_space.ocr(sample_image)
        assert text == sample_ocr_result
