from PIL import Image, ImageSequence
from io import BytesIO, StringIO
from contextlib import asynccontextmanager

asciiChars = ['@', '%', '#', '*',
                  '+', '=', '-', ';', ':', ',', '.']

@asynccontextmanager
async def asyncToAscii(image_bytes: BytesIO):
    with Image.open(image_bytes) as img:
        img = img.convert('L')

        width, height = img.size
        aspect_ratio = height/width
        new_width = 120
        new_height = aspect_ratio * new_width * 0.55
        img = img.resize((new_width, int(new_height)))

        imageArray = img.getdata()

        pixels = ''.join([asciiChars[pixel//25]
                            for pixel in imageArray])
        asciiImg = '\n'.join([pixels[index:index+new_width]
                                for index in range(0, len(pixels), new_width)])

        txt = StringIO()
        txt.write(asciiImg)
        txt.seek(0)
        yield txt


def resolve_ascii(type):
    if (ext in type for ext in ('png', 'jpeg', 'jpg')):
        return asyncToAscii