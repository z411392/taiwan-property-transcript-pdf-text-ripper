import pytest
from app.bootstrap import bootstrap
from app.container import Container
from app.infrastructure.hashers.bytes_hasher import BytesHasher


@pytest.mark.skip
class TestBytesHasher:
    @pytest.fixture
    async def container(self):
        async with bootstrap() as container:
            yield container

    @pytest.fixture
    async def bytes_hasher(self, container: Container):
        return container.bytes_hasher()

    # @pytest.mark.skip
    @pytest.mark.describe("要能夠產生 bytes 的 uuid")
    async def test_bytes_uuid(
        self,
        bytes_hasher: BytesHasher,
        sample_image: bytes,
        sample_image_hash: str,
    ):
        hash = bytes_hasher(sample_image)
        assert hash == sample_image_hash
