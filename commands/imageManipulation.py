from discord.ext.commands import Cog
from discord import File, Attachment, app_commands, Interaction

from .resources.exceptions import CustomCheckError

from io import BytesIO
from aiohttp import ClientSession

from re import compile

from .resources.image_manipulation.shakal import resolve_shakal
from .resources.image_manipulation.ascii import resolve_ascii
from .resources.image_manipulation.demotivator import resolve_demotivator

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

    @app_commands.command(name='ascii', description='Переводит картинку в ascii текст')
    async def ascii(self, inter: Interaction, image_url: str = None, attachment: Attachment = None):
        if not image_url and not attachment:
            raise CustomCheckError(message="Ссылка не найдена")

        image_url = image_url or attachment.url
        if not self.urlValid.match(image_url):
            raise CustomCheckError(message="Ссылка не найдена")

        filetype, _ = await self.get_file_info(image_url)
        ascii_func = resolve_ascii(filetype)
        if not ascii_func:
            raise CustomCheckError(message="Неподдерживаемый формат файла - доступны png, jpeg и jpg")

        image_bytes = BytesIO(await self.get_bytes_from_url(image_url))

        txt = await self.bot.loop.run_in_executor(None, ascii_func, image_bytes)

        await inter.response.send_message(file=File(fp=txt, filename="now.txt"))
        
    @app_commands.command(name='demotivator', description='Как в мемах. Нужна ссылка')
    async def demotivator(self, inter: Interaction, text: str, image_url: str = None, attachment: Attachment = None):
        if not image_url and not attachment:
            raise CustomCheckError(message="Ссылка не найдена")

        image_url = image_url or attachment.url
        if not self.urlValid.match(image_url):
            raise CustomCheckError(message="Ссылка не найдена")

        if len(text) > 25:
            raise CustomCheckError(message="Введите не более 25 символов")

        filetype, _ = await self.get_file_info(image_url)

        demotivator_func = resolve_demotivator(filetype)
        if not demotivator_func:
            raise CustomCheckError(message="Неподдерживаемый формат файла - доступны png, jpeg и jpg")
        
        image_bytes = BytesIO(await self.get_bytes_from_url(image_url))
        demotiv_img = await self.bot.loop.run_in_executor(None, demotivator_func, image_bytes, text)
        await inter.response.send_message(file=File(fp=demotiv_img, filename="now.jpeg"))
        
    @app_commands.command(name='shakalizator', description='Надо прикрепить фотку или гиф.')
    async def shakalizator(self, inter: Interaction, image_url: str = None, attachment: Attachment = None):
        if not image_url and not attachment:
            raise CustomCheckError(message="Ссылка не найдена")
        
        image_url = image_url or attachment.url

        if not self.urlValid.match(image_url):
            raise CustomCheckError(message="Ссылка не найдена")

        filetype, length = await self.get_file_info(image_url)
        
        shakalizator_func = resolve_shakal(filetype)
        if not shakalizator_func:
            raise CustomCheckError(message="Неподдерживаемый формат файла - доступны png, jpeg, jpg, gif")

        if length > FIVE_MEGABYTES:
            raise CustomCheckError(message="Максимальный размер файла - 5МБ")
        
        image_bytes = BytesIO(await self.get_bytes_from_url(image_url))

        shakalized = await self.bot.loop.run_in_executor(None, shakalizator_func, image_bytes)
        await inter.response.send_message(file=File(fp=shakalized, filename=f'now.{filetype}'))

async def setup(bot):
    await bot.add_cog(ImageManipulation(bot))
