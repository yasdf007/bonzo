from discord.ext.commands import Cog, command, hybrid_command
from discord.ext.commands.context import Context
from random import randint

name = "randomcat"
description = "Отправляет случайного котика :3"


class randomCat(Cog):
    def __init__(self, bot):
        self.bot = bot

    @hybrid_command(name=name, description=description)
    async def randomcat(self, ctx, num: int = 1):
        if int(num) > 2:
            num = 2
        # Делаем Num ссылок
        for _ in range(0, num):
            cat = await self.makeCatUrl()
            await ctx.send(cat)

    # Функци создания картинки

    async def makeCatUrl(self):
        return "https://cataas.com/cat?" + str(randint(0, 10 ** 6))


async def setup(bot):
    await bot.add_cog(randomCat(bot))
