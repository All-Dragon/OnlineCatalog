from boto3.session import Session as BotoSession
from botocore.client import BaseClient
from botocore.config import Config
from botocore.exceptions import ClientError

from app.core.config import Settings


def create_s3_client(settings: Settings) -> BaseClient:
    session = BotoSession()

    return session.client(
        "s3",
        endpoint_url=settings.s3_endpoint_url,
        region_name=settings.s3_region,
        aws_access_key_id=settings.s3_access_key,
        aws_secret_access_key=settings.s3_secret_key.get_secret_value(),
        config=Config(
            signature_version="s3v4",
            s3={"addressing_style": "path"},
            connect_timeout=3,
            read_timeout=10,
        ),
    )


def ensure_bucket(client: BaseClient, name: str) -> None:
    try:
        client.head_bucket(Bucket=name)
        return
    except ClientError as error:
        status_code = error.response["ResponseMetadata"]["HTTPStatusCode"]
        if status_code != 404:
            raise

    try:
        client.create_bucket(Bucket=name)
    except ClientError as error:
        error_code = error.response["Error"]["Code"]
        if error_code not in {
            "BucketAlreadyOwnedByYou",
            "BucketAlreadyExists",
        }:
            raise

    client.head_bucket(Bucket=name)
