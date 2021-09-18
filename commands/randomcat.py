from discord.ext.commands import Cog
from random import randint
from discord_slash import SlashContext, cog_ext
from config import guilds

name = 'randomcat'
description = 'Отправляет случайного котика :3'


class randomCat(Cog):
    def __init__(self, bot):
        self.bot = bot

    # Обработа ошибок
    @cog_ext.cog_slash(name=name, description=description, guild_ids=guilds)
    async def randomcat(self, ctx: SlashContext, num: int = 1):
        if int(num) > 2:
            num = 2
        # Делаем Num ссылок
        for _ in range(0, num):
            cat = await self.makeCatUrl()
            await ctx.send(cat)
    # Функци создания картинки

    async def makeCatUrl(self):
        return 'https://cataas.com/cat?' + str(randint(0, 10**6))


def setup(bot):
    bot.add_cog(randomCat(bot))
