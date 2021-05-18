from discord.ext.commands import Cog, CommandInvokeError, CommandOnCooldown, cooldown, command, BucketType
from discord import File
from PIL import Image, ImageSequence
from io import BytesIO
from aiohttp import ClientSession
from re import compile
name = 'shakalizator'
description = 'Надо прикрепить фотку или гиф.'


class Shakalizator(Cog):
    urlValid = compile(r'https?://(?:www\.)?.+')

    def __init__(self, bot):
        self.bot = bot

    # Обработка ошибок
    async def cog_command_error(self, ctx, error):
        if isinstance(error, CommandInvokeError):
            await ctx.message.reply(error.original)

        if isinstance(error, CommandOnCooldown):
            await ctx.message.reply(error)

    @cooldown(rate=1, per=5, type=BucketType.user)
    @command(name=name, description=description, aliases=['шакал', 'сжать', 'shakal'])
    async def shakalizator(self, ctx, imageUrl=None):
        imageUrl = imageUrl or ctx.message.attachments[0].url

        if not self.urlValid.match(imageUrl):
            raise CommandInvokeError('Ссылка не найдена')

        async with ClientSession() as session:
            async with session.head(imageUrl) as response:
                fileType = response.content_type.split('/')[-1]

        if 'gif' in fileType:
            await (await self.bot.loop.run_in_executor(None, self.asyncGifShakalizator, ctx, imageUrl))

        # Один из форматов
        elif any(ext in fileType for ext in ('png', 'jpeg', 'jpg')):
            await (await self.bot.loop.run_in_executor(None, self.asyncPhotoShakalizator, ctx, imageUrl))
        else:
            raise CommandInvokeError(
                f'Поддерживаемые форматы: png, jpeg, jpg, gif. У тебя {fileType}')

    async def asyncGifShakalizator(self, ctx, url):
        async with ClientSession() as session:
            async with session.get(url) as response:
                try:
                    requestImage = await response.read()
                except:
                    raise CommandInvokeError('Не удалось открыть файл')

        bytes = BytesIO(requestImage)
        bytes.seek(0, 2)

        if bytes.tell() >= 5242880:
            raise CommandInvokeError('Максимальный размер гифки 5 мегабайт')

        img = Image.open(bytes)

        frames = [frame.resize((int(img.size[0] / 8), int(img.size[1] / 8)))
                  for frame in ImageSequence.Iterator(img)]

        frames = [frame.resize((300, 300))
                  for frame in frames]

        with BytesIO() as image_binary:
            frames[0].save(image_binary, format='GIF', save_all=True,
                           append_images=frames[1:], optimize=False, duration=100, loop=0)

            image_binary.seek(0)

            await ctx.message.reply(file=File(fp=image_binary, filename='now.gif'))

    async def asyncPhotoShakalizator(self, ctx, imageUrl):
        async with ClientSession() as session:
            async with session.get(imageUrl) as response:
                try:
                    requestImage = await response.read()
                except:
                    raise CommandInvokeError('Не удалось открыть файл')

        # Открываем фотку в RGB формате (фотки без фона ARGB ломают все)
        img = Image.open(BytesIO(requestImage))
        img = img.convert('RGB')

        # Изменение фотки
        img = img.resize((int(img.size[0] / 2), int(img.size[1] / 2)))

        # Создаем новую фотку
        with BytesIO() as image_binary:
            # Шакалим
            img.save(image_binary, "jpeg", quality=0)
            image_binary.seek(0)
            await ctx.message.reply(file=File(fp=image_binary, filename='now.jpeg'))


def setup(bot):
    bot.add_cog(Shakalizator(bot))
