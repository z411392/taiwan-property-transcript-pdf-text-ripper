from pymupdf import Document
from unicodedata import normalize
from re import sub
from typing import AsyncGenerator, Tuple


class PDFTextRipper:
    _pdf: bytes

    def __init__(self, pdf: bytes):
        self._pdf = pdf

    async def __aiter__(self) -> AsyncGenerator[Tuple[bool, str], None]:
        doc = Document(stream=self._pdf)
        for page in doc:
            page_data = page.get_text("dict")
            blocks = page_data["blocks"]
            for block in blocks:
                if block["type"] == 0:
                    for content in self._process_text_block(block):
                        yield False, content
                if block["type"] == 1:
                    yield True, block["image"]

    def _process_text_block(self, block):
        for line in block["lines"]:
            for span in line["spans"]:
                text: str = span["text"]
                normalized = sub(r"\((.)\)", r"\1", normalize("NFKD", text))
                content = normalized.strip()
                if content:
                    yield content
