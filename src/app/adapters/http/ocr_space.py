from base64 import b64encode
from aiohttp import ClientSession


class OCRSpace:
    _api_key: str
    _endpoint: str = "https://api.ocr.space/parse/image"

    def __init__(self, /, api_key: str):
        self._api_key = api_key

    async def ocr(self, image: bytes, language: str = "cht"):
        base64_encoded = b64encode(image).decode("utf-8")
        base64_image = f"data:image/jpeg;base64,{base64_encoded}"
        body = {
            "apikey": self._api_key,
            "language": language,
            "base64Image": base64_image,
        }
        async with ClientSession() as session:
            async with session.post(self._endpoint, data=body) as response:
                payload = await response.json()
                if "ParsedResults" not in payload:
                    return ""
                results = payload["ParsedResults"]
                joined = "".join((result["ParsedText"] for result in results))
                trimed = joined.replace("\r", "").replace("\n", "").strip()
                return trimed
