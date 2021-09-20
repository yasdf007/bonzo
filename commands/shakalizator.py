from discord.ext.commands import Cog, command
from discord.ext.commands.context import Context
from discord.ext.commands.errors import MissingRequiredArgument
from typing import Optional
from discord import File
from PIL import Image, ImageSequence
from io import BytesIO
from aiohttp import ClientSession
from discord_slash import SlashContext, cog_ext
from config import guilds
from re import compile

name = 'shakalizator'
description = 'Надо прикрепить фотку или гиф.'


class Shakalizator(Cog):
    urlValid = compile(r'https?://(?:www\.)?.+')

    def __init__(self, bot):
        self.bot = bot

    async def cog_command_error(self, ctx, error):
        if isinstance(error, MissingRequiredArgument):
            await ctx.send('Нужно указать текст/ссылку')

    @command(name=name, description=description, aliases=['шакал', 'сжать', 'shakal'])
    async def shakalizator_prefix(self, ctx: Context, img_url: Optional[str]):
        img_url = img_url or (ctx.message.attachments[0].url if len(
            ctx.message.attachments) > 0 else '')
        await self.shakalizator(ctx, img_url)

    @cog_ext.cog_slash(name=name, description=description)
    async def shakalizator_slash(self, ctx: SlashContext, image_url: str):
        await self.shakalizator(ctx, image_url)

    async def shakalizator(self, ctx, image_url: str):

        async with ClientSession() as session:
            async with session.head(image_url) as response:
                fileType = response.content_type.split('/')[-1]

        if 'gif' in fileType:
            await (await self.bot.loop.run_in_executor(None, self.asyncGifShakalizator, ctx, image_url))

        # Один из форматов
        elif any(ext in fileType for ext in ('png', 'jpeg', 'jpg')):
            await (await self.bot.loop.run_in_executor(None, self.asyncPhotoShakalizator, ctx, image_url))
        else:
            await ctx.send(
                f'Поддерживаемые форматы: png, jpeg, jpg, gif. У тебя {fileType}')
            return

    async def asyncGifShakalizator(self, ctx, url):
        async with ClientSession() as session:
            async with session.get(url) as response:
                try:
                    requestImage = await response.read()
                except:
                    await ctx.send('Не удалось открыть файл')
                    return

        bytes = BytesIO(requestImage)
        bytes.seek(0, 2)

        if bytes.tell() >= 5242880:
            await ctx.send('Максимальный размер гифки 5 мегабайт')
            return

        with Image.open(bytes) as img:

            frames = [frame.resize((int(img.size[0] // 8), int(img.size[1] // 8))).resize((300, 300))
                      for frame in ImageSequence.Iterator(img)]

            with BytesIO() as image_binary:
                frames[0].save(image_binary, format='GIF', save_all=True,
                               append_images=frames[1:], optimize=False, duration=100, loop=0)

                image_binary.seek(0)

                await ctx.send(file=File(fp=image_binary, filename='now.gif'))

    async def asyncPhotoShakalizator(self, ctx, imageUrl):
        async with ClientSession() as session:
            async with session.get(imageUrl) as response:
                try:
                    requestImage = await response.read()
                except:
                    await ctx.send('Не удалось открыть файл')
                    return

        # Открываем фотку в RGB формате (фотки без фона ARGB ломают все)
        with Image.open(BytesIO(requestImage)) as img:
            img = img.convert('RGB')
            img.thumbnail((750, 750))
            # Изменение фотки
            img = img.resize((int(img.size[0] / 2), int(img.size[1] / 2)))

            # Создаем новую фотку
            with BytesIO() as image_binary:
                # Шакалим
                img.save(image_binary, "jpeg", quality=0)
                image_binary.seek(0)
                await ctx.send(file=File(fp=image_binary, filename='now.jpeg'))


def setup(bot):
    bot.add_cog(Shakalizator(bot))
