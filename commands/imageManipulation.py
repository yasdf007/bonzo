from discord.ext.commands import Cog
from discord.ext.commands import Cog, hybrid_command, Context
from discord import File, Attachment

from .resources.exceptions import CustomCheckError

from io import BytesIO
from aiohttp import ClientSession

from re import compile

from .resources.image_manipulation.shakal import resolve_shakal
from .resources.image_manipulation.ascii import resolve_ascii

from bot import Bot


ONE_MEGABYTE = 1024 * 1024

FIVE_MEGABYTES = 5 * ONE_MEGABYTE

class ImageManipulation(Cog):
    urlValid = compile(r'https?://(?:www\.)?.+')

    def __init__(self, bot):
        self.bot: Bot = bot

    async def get_bytes_from_url(self, url):
        async with ClientSession() as session:
            async with session.get(url) as response:
                return await response.read()

    async def get_file_info(self, url):
        async with ClientSession() as session:
            async with session.head(url) as response:
                return response.content_type.split('/')[-1], response.content_length

    @hybrid_command(name='ascii', description='Переводит картинку в ascii текст')
    async def ascii(self, ctx: Context, image_url: str = None, attachment: Attachment = None):
        if not image_url and not attachment:
            raise CustomCheckError(message="Ссылка не найдена")

        image_url = image_url or attachment.url
        if not self.urlValid.match(image_url):
            raise CustomCheckError(message="Ссылка не найдена")

        filetype, _ = await self.get_file_info(image_url)
        ascii = resolve_ascii(filetype)
        if not ascii:
            raise CustomCheckError(message="Неподдерживаемый формат файла - доступны png, jpeg и jpg")

        image_bytes = BytesIO(await self.get_bytes_from_url(image_url))

        async with ascii(image_bytes) as txt:
            await ctx.send(file=File(fp=txt, filename="now.txt"))
        

    # @hybrid_command(name='demotivator', description='Как в мемах. Нужна ссылка')
    # async def demotivator(self, ctx: Context, text, image_url: str = None, attachment: Attachment = None):
    #     image_url = image_url or attachment.url
    #     if not self.urlValid.match(image_url):
    #         raise NoUrlFound

    #     if len(text) > 25:
    #         raise CustomCheckError(message="Команда поддерживает не более 25 символов")

    #     filetype, _ = await self.get_file_info(image_url)

    #     demotivator = resolve_demotivator(filetype)
    #     if not demotivator:
    #         raise InvalidFileType

    #     image_bytes = BytesIO(await self.get_bytes_from_url(image_url))

    #     async with demotivator(image_bytes, text=text) as demotiv:
    #         await ctx.send(file=File(fp=demotiv, filename=f'now.{filetype}'))
        
    # async def asyncDemotivator(self, image_bytes, underText):

    #     img = Image.open(image_bytes)
    #     template = Image.open('./static/demotivatorTemplate.png')

    #     draw = ImageDraw.Draw(template)
    #     font = ImageFont.truetype('./static/arial.ttf', 54)
    #     textWidth = font.getsize(underText)[0]
    #     # Открываем фотку в RGB формате (фотки без фона ARGB ломают все)
    #     img = img.convert('RGB')
    #     img = img.resize((666, 655))

    #     template.paste(img, (50, 50))

    #     draw.text(((760 - textWidth) / 2, 720), underText, (255, 255, 255),
    #               font=font, align='right')

    #     with BytesIO() as temp:
    #         template.save(temp, "png", quality=100)
    #         temp.seek(0)
    #         await ctx.send(file=File(fp=temp, filename='now.png'))

    @hybrid_command(name='shakalizator', description='Надо прикрепить фотку или гиф.', aliases=['шакал', 'сжать', 'shakal'])
    async def shakalizator(self, ctx: Context, image_url: str = None, attachment: Attachment = None):
        if not image_url and not attachment:
            raise CustomCheckError(message="Ссылка не найдена")
        
        image_url = image_url or attachment.url

        if not self.urlValid.match(image_url):
            raise CustomCheckError(message="Ссылка не найдена")

        filetype, length = await self.get_file_info(image_url)

        
        shakalizator = resolve_shakal(filetype)
        if not shakalizator:
            raise CustomCheckError(message="Неподдерживаемый формат файла - доступны png, jpeg, jpg, gif")

        if length > FIVE_MEGABYTES:
            raise CustomCheckError(message="Максимальный размер файла - 5МБ")
        
        image_bytes = BytesIO(await self.get_bytes_from_url(image_url))

        async with shakalizator(image_bytes) as shakalized:
            await ctx.send(file=File(fp=shakalized, filename=f'now.{filetype}'))

async def setup(bot):
    await bot.add_cog(ImageManipulation(bot))
