from pymupdf import Document
from unicodedata import normalize
from re import sub


class PDFTextRipper:
    _pdf: bytes

    def __init__(self, pdf: bytes):
        self._pdf = pdf

    async def __aiter__(self) -> str:
        doc = Document(stream=self._pdf)
        for page in doc:
            dict = page.get_text("dict")
            blocks = dict["blocks"]
            for block in blocks:
                if block["type"] == 0:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            text: str = span["text"]
                            normalized = sub(r"\((.)\)", r"\1", normalize("NFKD", text))
                            content = normalized.strip()
                            if content:
                                yield False, content
                if block["type"] == 1:
                    yield True, block["image"]
