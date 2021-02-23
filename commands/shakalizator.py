from discord.ext.commands import Cog, CommandInvokeError, CommandOnCooldown, cooldown, command
from discord import File
from PIL import Image
from io import BytesIO
import requests

name = 'shakalizator'
description = 'ОПЯТЬ СЖИМАЕШЬ ШАКАЛ. Надо прикрепить фотку или ссылку'


class Shakalizator(Cog):
    def __init__(self, bot):
        self.bot = bot

    # Обработка ошибок
    async def cog_command_error(self, ctx, error):
        if isinstance(error, CommandInvokeError):
            await ctx.message.reply('Где фотка')

        if isinstance(error, CommandOnCooldown):
            await ctx.message.reply(error)

    @cooldown(rate=1, per=5)
    @command(name=name, description=description, aliases=['шакал', 'сжать', 'shakal'])
    async def shakalizator(self, ctx, imageUrl=None):
        # Если нет прикрепленной фотки, то обрабатываем фото из ссылки
        if imageUrl != None:
            requestImage = requests.get(imageUrl)
        # Если нет ссылки, то берем прикладываемую
        elif ctx.message.attachments:
            urlFromPhoto = ctx.message.attachments[0].url
            requestImage = requests.get(urlFromPhoto)
        else:
            # Не вызывается поч
            raise CommandInvokeError()

        # Открываем фотку в RGB формате (фотки без фона ARGB ломают все)
        img = Image.open(BytesIO(requestImage.content))
        img = img.convert('RGB')

        # Изменение фотки
        img = img.resize((int(img.size[0] / 2), int(img.size[1] / 2)))

        # Изменение фотки

        # Создаем новую фотку
        with BytesIO() as image_binary:
            # Шакалим
            img.save(image_binary, "jpeg", quality=0)
            image_binary.seek(0)
            await ctx.message.reply(file=File(fp=image_binary, filename='now.jpeg'))


def setup(bot):
    bot.add_cog(Shakalizator(bot))
