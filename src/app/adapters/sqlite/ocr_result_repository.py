from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.schemas.general.ocr_results import OCRResult
from sqlalchemy import select
from sqlalchemy.dialects.sqlite import insert


class OCRResultRepository:
    _session: AsyncSession

    def __init__(self, session: AsyncSession):
        self._session = session

    async def save(self, id: str, text: str):
        stmt = insert(OCRResult).values(id=id, text=text)
        stmt = stmt.on_conflict_do_update(index_elements=["id"], set_={"text": text})
        await self._session.execute(stmt)
        await self._session.commit()

    async def load(self, id: str) -> str:
        result = await self._session.execute(
            select(OCRResult).where(OCRResult.id == id)
        )
        ocr_result = result.scalar()
        if ocr_result is None:
            return None
        return ocr_result.text
