import hashlib
from io import BytesIO
import shortuuid
from uuid import uuid5, UUID


class BytesHasher:
    _chunk_size: int

    def __init__(self, /, chunk_size: int = 8192) -> None:
        self._chunk_size = chunk_size

    def __call__(self, buffer: bytes, namespace: UUID | None = None) -> str:
        if namespace is None:
            namespace = UUID("00000000-0000-0000-0000-000000000000")
        md5 = hashlib.md5()
        io = BytesIO(buffer)
        while chunk := io.read(self._chunk_size):
            md5.update(chunk)
        uuid = uuid5(namespace, md5.digest())
        return shortuuid.encode(uuid)
