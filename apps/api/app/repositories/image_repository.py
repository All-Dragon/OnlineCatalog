import logging
from asyncio import to_thread
from contextlib import closing
from dataclasses import dataclass

from botocore.client import BaseClient
from botocore.exceptions import (
    BotoCoreError,
    ClientError,
    ConnectTimeoutError,
    EndpointConnectionError,
    HTTPClientError,
    IncompleteReadError,
)

from app.core.exceptions import (
    ImageNotFoundError,
    StorageError,
    StorageUnavailableError,
)

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
            try:
                await to_thread(
                    self._client.put_object,
                    Bucket=self._bucket_name,
                    Key=key,
                    Body=data,
                    ContentType=content_type,
                )
            except ClientError as error:
                code = error.response.get("Error", {}).get("Code")
                status_code = error.response.get(
                    "ResponseMetadata", {}
                ).get("HTTPStatusCode", 0)

                if status_code >= 500 or status_code == 429 or code in {
                    "SlowDown",
                    "RequestTimeout",
                }:
                    raise StorageUnavailableError(
                        "Image storage is temporarily unavailable"
                    ) from error

                raise StorageError("Failed to upload image") from error
            except (
                EndpointConnectionError,
                ConnectTimeoutError,
                HTTPClientError,
            ) as error:
                raise StorageUnavailableError(
                    "Failed to upload image to storage"
                ) from error
            except BotoCoreError as error:
                raise StorageError("Failed to upload image") from error

            logger.debug(
                "Uploaded image: bucket=%s key=%s size=%s",
                self._bucket_name,
                key,
                len(data),
            )

    async def download(self, key: str) -> ImageData:
        try:
            image = await to_thread(self._download, key)
        except ClientError as error:
            code = error.response.get("Error", {}).get("Code")
            status_code = error.response.get(
                "ResponseMetadata", {}
            ).get("HTTPStatusCode", 0)

            if code == "NoSuchKey":
                raise ImageNotFoundError(
                    f"Image not found: {key}"
                ) from error

            if status_code >= 500 or status_code == 429 or code in {
                "SlowDown",
                "RequestTimeout",
            }:
                raise StorageUnavailableError(
                    "Image storage is temporarily unavailable"
                ) from error

            raise StorageError("Failed to download image") from error
        except (
            EndpointConnectionError,
            ConnectTimeoutError,
            HTTPClientError,
            IncompleteReadError,
        ) as error:
            raise StorageUnavailableError(
                "Failed to receive image from storage"
            ) from error
        except BotoCoreError as error:
            raise StorageError("Failed to download image") from error

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
