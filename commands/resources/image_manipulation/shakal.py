from PIL import Image, ImageSequence
from io import BytesIO
from contextlib import asynccontextmanager

@asynccontextmanager
async def asyncGifShakalizator(image_bytes: BytesIO):
    with Image.open(image_bytes) as img:
        frames = [frame.resize((int(img.size[0] // 8), int(img.size[1] // 8))).resize((300, 300))
                    for frame in ImageSequence.Iterator(img)]

        image_binary =  BytesIO()

        frames[0].save(image_binary, format='GIF', save_all=True,
                        append_images=frames[1:], optimize=False, duration=100, loop=0)

        image_binary.seek(0)
        yield image_binary

@asynccontextmanager
async def asyncPhotoShakalizator(image_bytes: BytesIO):
    with Image.open(image_bytes) as img:
        img = img.convert('RGB')
        img.thumbnail((750, 750))
        # Изменение фотки
        img = img.resize((int(img.size[0] / 2), int(img.size[1] / 2)))
        
        image_binary = BytesIO()
        img.save(image_binary, "jpeg", quality=0)
        image_binary.seek(0)
        yield image_binary

def resolve_shakal(type):
    if 'gif' in type:
        return asyncGifShakalizator
    elif any(ext in type for ext in ('png', 'jpeg', 'jpg')):
        return asyncPhotoShakalizator