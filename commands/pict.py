from discord.ext.commands import Cog
from random import choices
from typing import Optional
from string import ascii_lowercase, digits
from discord_slash import SlashContext, cog_ext
from config import guilds

name = 'pict'
description = 'Отправляет случайное изображение из prnt.sc :o'


class pict(Cog):
    url = 'https://prnt.sc/'

    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name=name, description=description)
    async def pict(self, ctx: SlashContext, num: int = 1):
        if int(num) > 2:
            num = 2
        for _ in range(0, num):
            url = await self.makePictUrl()
            await ctx.send(url)

    # Функция, генерирующая ссылку
    async def makePictUrl(self):
        # делаем случайную строку из 6 символов
        symbolsStr = ''.join(choices(ascii_lowercase + digits, k=6))
        # соединяем строку с ссылкой url
        result = self.url + symbolsStr
        return result


def setup(bot):
    bot.add_cog(pict(bot))
