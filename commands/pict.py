from discord.ext.commands import Cog, hybrid_command, Context
from random import choices
from string import ascii_lowercase, digits
from bot import Bot

name = "pict"
description = "Отправляет случайное изображение из prnt.sc :o"


class pict(Cog):
    url = "https://prnt.sc/"

    def __init__(self, bot):
        self.bot: Bot = bot

    @hybrid_command(name=name, description=description)
    async def pict(self, ctx: Context, num: int = 1):
        if int(num) > 2:
            num = 2
        for _ in range(0, num):
            url = await self.makePictUrl()
            await ctx.send(url)

    # Функция, генерирующая ссылку
    async def makePictUrl(self):
        # делаем случайную строку из 6 символов
        symbolsStr = "".join(choices(ascii_lowercase + digits, k=6))
        # соединяем строку с ссылкой url
        result = self.url + symbolsStr
        return result


async def setup(bot):
    await bot.add_cog(pict(bot))
