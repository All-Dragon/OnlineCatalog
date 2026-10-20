import logging
from asyncio import to_thread
from contextlib import closing
from dataclasses import dataclass

from botocore.client import BaseClient


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ImageData:
    data: bytes
    content_type: str


class ImageRepository:
    def __init__(self, client: BaseClient, bucket_name: str) -> None:
        self._client = client
        self._bucket_name = bucket_name

    async def upload(
        self,
        key: str,
        data: bytes,
        content_type: str,
    ) -> None:
        await to_thread(
            self._client.put_object,
            Bucket=self._bucket_name,
            Key=key,
            Body=data,
            ContentType=content_type,
        )

        logger.debug(
            "Uploaded image: bucket=%s key=%s size=%s",
            self._bucket_name,
            key,
            len(data),
        )

    async def download(self, key: str) -> ImageData:
        image = await to_thread(self._download, key)

        logger.debug(
            "Downloaded image: bucket=%s key=%s size=%s",
            self._bucket_name,
            key,
            len(image.data),
        )

        return image

    def _download(self, key: str) -> ImageData:
        response = self._client.get_object(
            Bucket=self._bucket_name,
            Key=key,
        )

        with closing(response["Body"]) as body:
            data = body.read()

        return ImageData(
            data=data,
            content_type=response.get(
                "ContentType",
                "application/octet-stream",
            ),
        )
