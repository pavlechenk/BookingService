import aiofiles
from fastapi import APIRouter, UploadFile, status

from app.tasks.tasks import process_picture

router = APIRouter(prefix="/images", tags=["Загрузка картинок"])


@router.post("/hotels", status_code=status.HTTP_201_CREATED)
async def add_hotel_image(name: int, upload_file: UploadFile):
    image_path = f"app/static/images/{name}.webp"
    async with aiofiles.open(image_path, "wb+") as file_obj:
        file = await upload_file.read()
        await file_obj.write(file)

    process_picture.delay(image_path)
