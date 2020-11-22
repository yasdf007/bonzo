from discord.ext import commands
from discord import File
from PIL import Image
from io import BytesIO
from discord.ext.commands.errors import CommandInvokeError
import requests


class Shakalizator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Обработка ошибок
    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send('Где фотка')

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(error)

    @commands.cooldown(rate=1, per=5)
    @commands.command(name='shakalizator', description='ОПЯТЬ СЖИМАЕШЬ ШАКАЛ. Надо прикрепить фотку или ссылку', aliases=['шакал', 'сжать', 'shakal'])
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
            raise commands.CommandInvokeError()

        # Открываем фотку в RGB формате (фотки без фона ARGB ломают все)
        img = Image.open(BytesIO(requestImage.content))
        img = img.convert('RGB')
        # Изменение фотки
        img = img.resize((450, 450))

        # Создаем новую фотку
        with BytesIO() as image_binary:
            # Шакалим
            img.save(image_binary, "jpeg", quality=0)
            image_binary.seek(0)
            await ctx.send(file=File(fp=image_binary, filename='now.jpeg'))


def setup(bot):
    bot.add_cog(Shakalizator(bot))
