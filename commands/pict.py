from discord.ext.commands import Cog, command
from discord.ext.commands.context import Context
from random import choices
from string import ascii_lowercase, digits
from discord_slash import SlashContext, cog_ext
from config import guilds

name = 'pict'
description = 'Отправляет случайное изображение из prnt.sc :o'


class pict(Cog):
    url = 'https://prnt.sc/'

    def __init__(self, bot):
        self.bot = bot

    @command(name=name, description=description)
    async def pict_prefix(self, ctx: Context, num: int = 1):
        await self.pict(ctx, num)

    @cog_ext.cog_slash(name=name, description=description)
    async def pict_slash(self, ctx: SlashContext, num: int = 1):
        await self.pict(ctx, num)

    async def pict(self, ctx, num: int = 1):
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
