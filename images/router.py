from fastapi import APIRouter, UploadFile, status
import aiofiles

router = APIRouter(
    prefix='/images',
    tags=['Загрузка картинок']
)


@router.post('/hotels', status_code=status.HTTP_201_CREATED)
async def add_hotel_image(name: int, upload_file: UploadFile):
    async with aiofiles.open(f'app/static/images/{name}.webp', 'wb+') as file_obj:
        file = await upload_file.read()
        await file_obj.write(file)
