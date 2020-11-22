from discord.ext import commands
from random import randint


class randomCat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send('Нужно ввести количество ссылок (до 2)')

    @commands.command(name='randomcat', description='Отправляет случайного котика :3')
    async def randomcat(self, ctx, Num=None):
        if Num is None:
            cat = await self.makeCatUrl()
            await ctx.send(cat)
        else:
            Num = int(Num)

            if Num > 2:
                raise commands.CommandInvokeError()

            else:
                for _ in range(0, Num):
                    cat = await self.makeCatUrl()
                    await ctx.send(cat)

    async def makeCatUrl(self):
        return 'https://cataas.com/cat?' + str(randint(0, 10**6))


def setup(bot):
    bot.add_cog(randomCat(bot))
