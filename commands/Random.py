from discord import app_commands, Interaction
from discord.ext.commands import Cog, GroupCog
from bot import Bot
import random
from string import ascii_lowercase, digits
from aiohttp import ClientSession

class Random(GroupCog, group_name='random', group_description='Различные случайные данные'):
    def __init__(self, bot):
        self.bot: Bot = bot

    @app_commands.command(name='cat', description='Отправляет случайного кота')
    async def random_cat(self, inter: Interaction):
        await inter.response.send_message("https://cataas.com/cat")
    
    @app_commands.command(name='prntsc', description='Отправляет случайное изображение из https://prnt.sc')
    async def random_prntsc(self, inter: Interaction):
        symbolsStr = "".join(random.choices(ascii_lowercase + digits, k=6))
        await inter.response.send_message(f"https://prnt.sc/{symbolsStr}")

    @app_commands.command(name='imgur', description='Отправляет случайное изображение из https://imgur.com')
    async def random_imgur(self, inter: Interaction):
        photo = await self.process_imgur()

        while photo == None:
            photo = await self.process_imgur()

        await inter.response.send_message(photo)

    async def process_imgur(self):
        url = "https://i.imgur.com/"
        symbols = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

        # Генерируем 5 рандомных  символов
        randSymbols = "".join(random.sample(symbols, 5))

        # Делаем ссылку на картинку
        iImgurUrl = url + randSymbols + ".png"

        # Получаем инфу об картинке
        async with ClientSession() as session:
            async with session.head(iImgurUrl) as response:
                res = response

        # Если картинки нет, то она имеет размер 161х81 (размер 0 на сервере)
        if res.headers["content-length"] == "0":
            return None
        else:
            # Картинка нашлась, отправляем ссылку на картинку
            return iImgurUrl

async def setup(bot):
    await bot.add_cog(Random(bot))
