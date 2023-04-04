from commands.resources.AutomatedMessages import automata
from discord.ext.commands import Cog
from discord.ext.commands.errors import MissingRequiredArgument, MissingRequiredAttachment
from discord.ext.commands import Cog, command, CommandError, hybrid_command
from discord.ext.commands.context import Context
from discord import File, Attachment

from PIL import Image, ImageDraw, ImageFont, ImageSequence
from io import BytesIO, StringIO
from aiohttp import ClientSession

from re import compile


class NoUrlFound(CommandError):
    pass


class InvalidFileType(CommandError):
    pass


class RequestNetworkError(CommandError):
    pass


class TooManySymblos(CommandError):
    pass


class FileTooLarge(CommandError):
    pass


class ImageManipulation(Cog):
    urlValid = compile(r'https?://(?:www\.)?.+')
    asciiChars = ['@', '%', '#', '*',
                  '+', '=', '-', ';', ':', ',', '.']

    def __init__(self, bot):
        self.bot = bot

    async def cog_command_error(self, ctx, error):
        if isinstance(error, (NoUrlFound, MissingRequiredArgument)):
            return await ctx.send(embed=automata.generateEmbErr("Ссылка не найдена", error=error))

        if isinstance(error, InvalidFileType):
            return await ctx.send(embed=automata.generateEmbErr("Неподдерживаемый формат файла - доступны png, jpeg и jpg", error=error))

        if isinstance(error, RequestNetworkError):
            return await ctx.send(embed=automata.generateEmbErr("Не удалось открыть файл", error=error))

        if isinstance(error, TooManySymblos):
            return await ctx.send(embed=automata.generateEmbErr("Команда поддерживает не более 25 символов", error=error))

        if isinstance(error, FileTooLarge):
            return await ctx.send(embed=automata.generateEmbErr("Максимальный размер файла - 5МБ", error=error))

        if isinstance(error, MissingRequiredAttachment):
            return await ctx.send(embed=automata.generateEmbErr("Необходимо приложить файл", error=error))

        raise error

    @hybrid_command(name='ascii', description='Переводит картинку в ascii текст')
    async def ascii(self, ctx, image_url: str = None, attachment: Attachment = None):
        image_url = image_url or attachment.url
        if not self.urlValid.match(image_url):
            raise NoUrlFound

        async with ClientSession() as session:
            async with session.head(image_url) as response:
                fileType = response.content_type.split('/')[-1]

        if not any(ext in fileType for ext in ('png', 'jpeg', 'jpg')):
            raise InvalidFileType(fileType)

        await (await self.bot.loop.run_in_executor(None, self.asyncToAscii, ctx, image_url))

    async def asyncToAscii(self, ctx, url: str):
        async with ClientSession() as session:
            async with session.get(url) as response:
                try:
                    requestImage = await response.read()
                except:
                    raise RequestNetworkError

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

    @hybrid_command(name='demotivator', description='Как в мемах. Нужна ссылка')
    async def demotivator(self, ctx, text, image_url: str = None, attachment: Attachment = None):
        image_url = image_url or attachment.url
        if not self.urlValid.match(image_url):
            raise NoUrlFound

        if len(text) > 25:
            raise TooManySymblos

        async with ClientSession() as session:
            async with session.head(image_url) as response:
                fileType = response.content_type.split('/')[-1]

        if not any(ext in fileType for ext in ('png', 'jpeg', 'jpg')):
            raise InvalidFileType

        # O_O - первый await создает coroutine, второй его ждет и все работает
        await (await self.bot.loop.run_in_executor(None, self.asyncDemotivator, ctx, image_url, text))

    async def asyncDemotivator(self, ctx, image_url, underText):

        async with ClientSession() as session:
            async with session.get(image_url) as response:
                try:
                    photo = await response.read()
                except:
                    raise RequestNetworkError

        img = Image.open(BytesIO(photo))
        template = Image.open('./static/demotivatorTemplate.png')

        draw = ImageDraw.Draw(template)
        font = ImageFont.truetype('./static/arial.ttf', 54)
        textWidth = font.getsize(underText)[0]
        # Открываем фотку в RGB формате (фотки без фона ARGB ломают все)
        img = img.convert('RGB')
        img = img.resize((666, 655))

        template.paste(img, (50, 50))

        draw.text(((760 - textWidth) / 2, 720), underText, (255, 255, 255),
                  font=font, align='right')

        with BytesIO() as temp:
            template.save(temp, "png", quality=100)
            temp.seek(0)
            await ctx.send(file=File(fp=temp, filename='now.png'))


    @hybrid_command(name='shakalizator', description='Надо прикрепить фотку или гиф.', aliases=['шакал', 'сжать', 'shakal'])
    async def shakalizator(self, ctx, image_url: str = None, attachment: Attachment = None):
        image_url = image_url or attachment.url

        if not self.urlValid.match(image_url):
            raise NoUrlFound

        async with ClientSession() as session:
            async with session.head(image_url) as response:
                fileType = response.content_type.split('/')[-1]

        if 'gif' in fileType:
            await (await self.bot.loop.run_in_executor(None, self.asyncGifShakalizator, ctx, image_url))
        # Один из форматов
        elif any(ext in fileType for ext in ('png', 'jpeg', 'jpg')):
            await (await self.bot.loop.run_in_executor(None, self.asyncPhotoShakalizator, ctx, image_url))
        else:
            raise InvalidFileType(fileType)

    async def asyncGifShakalizator(self, ctx, url):
        async with ClientSession() as session:
            async with session.get(url) as response:
                try:
                    requestImage = await response.read()
                except:
                    raise RequestNetworkError

        bytes = BytesIO(requestImage)
        bytes.seek(0, 2)

        if bytes.tell() >= 5242880:
            raise FileTooLarge

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
                    raise RequestNetworkError

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


async def setup(bot):
    await bot.add_cog(ImageManipulation(bot))
