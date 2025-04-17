from pydantic import BaseModel
from app.adapters.http.ocr_space import OCRSpace
from app.infrastructure.media_handlers.document_handlers.pdf_text_ripper import (
    PDFTextRipper,
)
from io import StringIO
from app.adapters.sqlite.ocr_result_repository import OCRResultRepository
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from app.infrastructure.hashers.bytes_hasher import BytesHasher


class RippingPDFText(BaseModel):
    pdf: bytes


class RipPDFText:
    _ocr_space: OCRSpace
    _ocr_result_repository: OCRResultRepository
    _make_session: async_sessionmaker[AsyncSession]
    _bytes_hasher: BytesHasher

    def __init__(
        self,
        /,
        ocr_space: OCRSpace,
        ocr_result_repository: OCRResultRepository,
        make_session: async_sessionmaker[AsyncSession],
        bytes_hasher: BytesHasher,
    ):
        self._ocr_space = ocr_space
        self._ocr_result_repository = ocr_result_repository
        self._make_session = make_session
        self._bytes_hasher = bytes_hasher

    async def _ocr(self, content: bytes) -> str:
        async with self._make_session() as session:
            ocr_result_repository = OCRResultRepository(session=session)
            id = self._bytes_hasher(content)
            ocr_result = await ocr_result_repository.load(id)
            if ocr_result is not None:
                return ocr_result
            ocr_result = await self._ocr_space.ocr(content)
            await ocr_result_repository.save(id, ocr_result)
            return ocr_result

    async def __call__(self, ripping_pdf_text: RippingPDFText) -> str:
        pdf_text_ripper = PDFTextRipper(ripping_pdf_text.pdf)
        string = StringIO()
        async for is_image, content in pdf_text_ripper:
            if is_image:
                ocr_result = await self._ocr(content)
                string.write(f"\n{ocr_result}")
            else:
                string.write(f"\n{content}")
        return string.getvalue().strip()
