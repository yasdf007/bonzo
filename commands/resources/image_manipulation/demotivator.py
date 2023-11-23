from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

def bytes_to_demotivator(image_bytes: BytesIO, underText: str):
    with Image.open(image_bytes) as img:
        with Image.open('./static/demotivatorTemplate.png') as template:
            draw = ImageDraw.Draw(template)
            font = ImageFont.truetype('./static/arial.ttf', 54)

            textWidth = font.getlength(underText)

            # Открываем фотку в RGB формате (фотки без фона ARGB ломают все)
            img = img.convert('RGB')
            img = img.resize((666, 655))

            template.paste(img, (50, 50))

            draw.text(((760 - textWidth) / 2, 720), underText, (255, 255, 255),
                        font=font, align='right')
            
            image_binary = BytesIO()
            template.save(image_binary, "png", quality=100)
            image_binary.seek(0)
            return image_binary

def resolve_demotivator(type):
    if any(ext in type for ext in ('png', 'jpeg', 'jpg')):
        return bytes_to_demotivator