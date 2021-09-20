from discord.ext.commands import Cog, command
from discord.ext.commands.context import Context
from random import randint
from discord_slash import SlashContext, cog_ext
from config import guilds

name = 'randomcat'
description = 'Отправляет случайного котика :3'


class randomCat(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name=name, description=description)
    async def randomcat_prefix(self, ctx: Context, num: int = 1):
        await self.randomcat(ctx, num)

    @cog_ext.cog_slash(name=name, description=description)
    async def randomcat_slash(self, ctx: SlashContext, num: int = 1):
        await self.randomcat(ctx, num)

    async def randomcat(self, ctx, num: int = 1):
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
