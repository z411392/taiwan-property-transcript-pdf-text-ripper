from sqlalchemy import Column, String, DateTime
from datetime import datetime
from zoneinfo import ZoneInfo
from os import getenv
from app.infrastructure.schemas.general.base import Base


class OCRResult(Base):
    __tablename__ = "ocr_results"
    id = Column(String(22), primary_key=True)
    text = Column(String(32), nullable=False)
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(ZoneInfo(getenv("TZ")))
    )
