from pydantic import BaseModel


class Config(BaseModel):
    version: str
    ocr_space_api_key: str
    sqlite_db_path: str
