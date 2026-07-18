import asyncio
from contextlib import AsyncExitStack
from io import BytesIO
from typing import BinaryIO

from PIL import Image, UnidentifiedImageError
from aiobotocore.session import get_session
from fastapi import UploadFile
from types_aiobotocore_s3 import S3Client

from app.errors.storage import (
    ConvertImageError,
    StorageNotConnectedError,
    StorageUploadError,
)


def convert_to_webp(file: BinaryIO) -> BytesIO:
    file.seek(0)

    try:
        with Image.open(file) as image:
            if image.mode not in ("RGB", "RGBA"):
                image = image.convert("RGBA" if "A" in image.getbands() else "RGB")

            output = BytesIO()
            image.save(output, format="WEBP", quality=90, optimize=True)

        output.seek(0)
        return output
    except Exception:
        raise ConvertImageError()


class StorageService:
    def __init__(
        self, access_key: str, secret_key: str, endpoint_url: str, bucket_name: str
    ):
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url,
            "verify": False
        }

        self.bucket_name = bucket_name
        self.session = get_session()

        self.client: S3Client | None = None
        self.stack = AsyncExitStack()

    async def connect(self) -> None:
        try:
            self.client = await self.stack.enter_async_context(
                self.session.create_client("s3", **self.config)
            )
        except Exception:
            raise StorageNotConnectedError()

    async def close(self) -> None:
        await self.stack.aclose()

    async def upload_image(self, file: UploadFile, path: str):
        if self.client is None:
            raise StorageNotConnectedError()

        image = await asyncio.to_thread(convert_to_webp, file.file)

        try:
            await self.client.put_object(
                Bucket=self.bucket_name, Key=path, Body=image, ContentType="image/webp"
            )
        except Exception as exc:
            print(exc)
            raise StorageUploadError()
