from fastapi import HTTPException, UploadFile, status

from app.repositories.image_repository import ImageData


MAX_IMAGE_BYTES = 5 * 1024 * 1024


async def read_product_image(photo: UploadFile) -> ImageData:
    try:
        data = await photo.read(MAX_IMAGE_BYTES + 1)
    finally:
        await photo.close()

    if len(data) > MAX_IMAGE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_CONTENT_TOO_LARGE,
            detail="Image must not exceed 5 MiB",
        )

    if not data:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Image must not be empty",
        )

    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        content_type = "image/png"
    elif data.startswith(b"\xff\xd8\xff"):
        content_type = "image/jpeg"
    else:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Only JPEG and PNG images are supported",
        )

    return ImageData(
        data=data,
        content_type=content_type,
    )
