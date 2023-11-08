from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

from contextlib import asynccontextmanager

class ImageGeneration:
    template: Image.Image
    progress_bar: Image.Image
    font: ImageFont.FreeTypeFont

    def __init__(self):
        self.template = Image.open("./static/rankTemplate.png")
        self.progress_bar = Image.open("./static/progressBar.png")
        self.font = ImageFont.truetype("./static/arial.ttf", 14)

    def createMask(self, photo):
        with Image.new("L", photo.size, 0) as mask:
            drawMask = ImageDraw.Draw(mask)
            drawMask.ellipse((0, 0) + photo.size, fill=255)

            return mask

    def __enter__(self):
        return self

    def create_card(self, username: str, xp: int, xp_to_level_up: int, lvl: int, rank: int, photo_bytes: bytes, percents: float, all_ranks: int):
        fullBlack = (0, 0, 0)

        with Image.open(BytesIO(photo_bytes)) as user_pfp:
            template = self.template.copy()
            bar = self.progress_bar.copy()

            draw = ImageDraw.Draw(template)

            mask = self.createMask(user_pfp)

            avatarSize = (100, 100)

            rezised = user_pfp.resize(avatarSize)
            mask = mask.resize(avatarSize)

            barWidth = bar.size[0]
            croppedBar = bar.crop((0, 0, barWidth * (percents) / 100, 45))

            template.paste(rezised, (15, 15), mask)
            template.paste(croppedBar, (100, 255), croppedBar)

            percentsText = f"{percents}%"
            textWidth = self.font.getlength(percentsText)

            draw.text(
                ((650 - textWidth) / 2, 270),
                percentsText,
                fullBlack,
                font=self.font,
                align="right",
            )

            draw.text(
                (130, 12), f"{username}", fullBlack, font=self.font, align="center"
            )

            draw.text(
                (130, 43),
                f"RANK:{rank}/{all_ranks}",
                fullBlack,
                font=self.font,
                align="center",
            )

            draw.text(
                (130, 73),
                f"EXP: {xp}/{xp_to_level_up}",
                fullBlack,
                font=self.font,
                align="center",
            )

            draw.text(
                (130, 102), f"LVL: {lvl}", fullBlack, font=self.font, align="center"
            )
            
            b = BytesIO()
            template.save(b, "png")
            b.seek(0)

            return b
