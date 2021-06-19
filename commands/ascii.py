from discord.ext.commands import Cog, CommandInvokeError, CommandOnCooldown, cooldown, command, BucketType
from discord import File
from PIL import Image
from io import BytesIO, StringIO
from aiohttp import ClientSession
from re import compile


class Ascii(Cog):
    urlValid = compile(r'https?://(?:www\.)?.+')
    asciiChars = ['@', '%', '#', '*', '+', '=', '-', ';', ':', ',', '.']

    def __init__(self, bot):
        self.bot = bot

    async def cog_command_error(self, ctx, error):
        if isinstance(error, CommandInvokeError):
            await ctx.message.reply(error.original)

        if isinstance(error, CommandOnCooldown):
            await ctx.message.reply(error)

    @cooldown(rate=1, per=10, type=BucketType.user)
    @command(name='ascii', description='Переводит картинку в ascii текст (прикрепить фотку или ссылку)')
    async def ascii(self, ctx, imageUrl=None):
        imageUrl = imageUrl or ctx.message.attachments[0].url

        if not self.urlValid.match(imageUrl):
            raise CommandInvokeError('Ссылка не найдена')

        async with ClientSession() as session:
            async with session.head(imageUrl) as response:
                fileType = response.content_type.split('/')[-1]

        if any(ext in fileType for ext in ('png', 'jpeg', 'jpg')):
            await (await self.bot.loop.run_in_executor(None, self.asyncToAscii, ctx, imageUrl))
        else:
            raise CommandInvokeError(
                f'Поддерживаемые форматы: png, jpeg, jpg. У тебя {fileType}')

    async def asyncToAscii(self, ctx, url):
        async with ClientSession() as session:
            async with session.get(url) as response:
                try:
                    requestImage = await response.read()
                except:
                    raise CommandInvokeError('Не удалось открыть файл')

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
    bot.add_cog(Ascii(bot))
