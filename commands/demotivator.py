from discord.ext.commands import Cog, CommandInvokeError, CommandOnCooldown, BadArgument, cooldown, command
from discord import File
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from aiohttp import ClientSession
name = 'demotivator'
description = 'Как в мемах. Надо прикрепить фотку к сообщению (по ссылкам пока не работает)'


class Demotivator(Cog):
    def __init__(self, bot):
        self.bot = bot

    # Обработка ошибок
    async def cog_command_error(self, ctx, error):
        if isinstance(error, CommandInvokeError):
            await ctx.message.reply('Где фотка')

        if isinstance(error, CommandOnCooldown):
            await ctx.message.reply(error)

        if isinstance(error, BadArgument):
            await ctx.message.reply('Максимум 25 символов')

    @cooldown(rate=1, per=5)
    @command(name=name, description=description)
    async def demotivator(self, ctx, *text):
        underText = ' '.join(text)
        if len(underText) > 25:
            raise BadArgument()

        urlFromPhoto = ctx.message.attachments[0].url
        async with ClientSession() as session:
            async with session.get(urlFromPhoto) as response:
                requestImage = await response.read()

        img = Image.open(BytesIO(requestImage))
        img = img.convert('RGB')
        img = img.resize((666, 655))
        # Открываем фотку в RGB формате (фотки без фона ARGB ломают все)
        template = Image.open('./static/demotivatorTemplate.jpg')
        template.convert('RGB')

        template.paste(img, (50, 50))
        draw = ImageDraw.Draw(template)
        font = ImageFont.truetype('./static/arial.ttf', 54)
        textWidth = font.getsize(underText)[0]
        draw.text(((760 - textWidth) / 2, 720), underText, (255, 255, 255),
                  font=font, align='right')

        with BytesIO() as temp:
            template.save(temp, "jpeg", quality=100)
            temp.seek(0)
            await ctx.message.reply(file=File(fp=temp, filename='now.jpeg'))


def setup(bot):
    bot.add_cog(Demotivator(bot))
