from discord.ext.commands import Cog
from discord_slash import SlashContext, cog_ext
from discord import File
from PIL import Image
from io import BytesIO, StringIO
from aiohttp import ClientSession
from re import compile
from config import guilds
from discord.ext.commands import Cog, command
from discord.ext.commands.context import Context
from typing import Optional


class AsciiCog(Cog):
    urlValid = compile(r'https?://(?:www\.)?.+')
    asciiChars = ['@', '%', '#', '*',
                  '+', '=', '-', ';', ':', ',', '.']

    def __init__(self, bot):
        self.bot = bot

    @command(name='ascii', description='Переводит картинку в ascii текст')
    async def ascii_prefix(self, ctx: Context, img_url: Optional[str]):
        img_url = img_url or ctx.message.attachments[0].url if len(
            ctx.message.attachments) > 0 else ''
        await self.ascii(ctx, img_url)

    @cog_ext.cog_slash(name='ascii', description='Переводит картинку в ascii текст')
    async def ascii_slash(self, ctx: SlashContext, img_url: str):
        await self.ascii(ctx, img_url)

    async def ascii(self, ctx, img_url) -> None:

        if not self.urlValid.match(img_url):
            await ctx.send('Ссылка не найдена')
            return

        async with ClientSession() as session:
            async with session.head(img_url) as response:
                fileType = response.content_type.split('/')[-1]

        if not any(ext in fileType for ext in ('png', 'jpeg', 'jpg')):
            await ctx.send(f'Поддерживаемые форматы: png, jpeg, jpg. У тебя {fileType}')
            return

        await (await self.bot.loop.run_in_executor(None, self.asyncToAscii, ctx, img_url))

    async def asyncToAscii(self, ctx, url: str):
        async with ClientSession() as session:
            async with session.get(url) as response:
                try:
                    requestImage = await response.read()
                except:
                    await ctx.send('Не удалось открыть файл')
                    return

        with Image.open(BytesIO(requestImage)) as img:
            img = img.convert('L')

            width, height = img.size
            aspect_ratio = height/width
            new_width = 120
            new_height = aspect_ratio * new_width * 0.55
            img = img.resize((new_width, int(new_height)))

            imageArray = img.getdata()

            pixels = ''.join([self.asciiChars[pixel//25]
                              for pixel in imageArray])
            asciiImg = '\n'.join([pixels[index:index+new_width]
                                  for index in range(0, len(pixels), new_width)])

            with StringIO() as txt:
                txt.write(asciiImg)
                txt.seek(0)
                await ctx.send(file=File(fp=txt, filename="now.txt"))


def setup(bot):
    bot.add_cog(AsciiCog(bot))
