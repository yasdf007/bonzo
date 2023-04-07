from discord.ext.commands import Cog, hybrid_command, Context
from random import sample
from aiohttp import ClientSession
from bot import Bot

name = "randimg"
description = "Отправляет случайное изображение из imgur"


class randImg(Cog):
    def __init__(self, bot):
        self.bot: Bot = bot


    @hybrid_command(name=name, description=description)
    async def randimg(self, ctx: Context):
        photo = await self.process()

        while photo == None:
            photo = await self.process()

        await ctx.send(photo)

    async def process(self):
        url = "https://i.imgur.com/"
        symbols = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

        # Генерируем 5 рандомных  символов
        randSymbols = "".join(sample(symbols, 5))

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
    await bot.add_cog(randImg(bot))
