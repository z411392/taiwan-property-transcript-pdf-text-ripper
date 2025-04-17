from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration, Factory, Resource
from app.adapters.http.ocr_space import OCRSpace
from app.infrastructure.hashers.bytes_hasher import BytesHasher
from app.modules.text_ripping.application.rip_text import RipPDFText
from app.adapters.sqlite.ocr_result_repository import OCRResultRepository
from app.infrastructure.providers.sqlalchemy_session_provider import (
    provide_sqlalchemy_session,
)


class Container(DeclarativeContainer):
    config = Configuration()
    bytes_hasher = Factory(BytesHasher)
    ocr_space = Factory(OCRSpace, api_key=config.ocr_space_api_key)
    make_session = Resource(provide_sqlalchemy_session, config.sqlite_db_path)
    """
    rip_pdf_text
    """
    ocr_result_repository = Factory(OCRResultRepository, session=make_session)
    rip_pdf_text = Factory(
        RipPDFText,
        ocr_space=ocr_space,
        ocr_result_repository=ocr_result_repository,
        make_session=make_session,
        bytes_hasher=bytes_hasher,
    )
