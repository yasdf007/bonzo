from discord.ext import commands
from random import randint


class randomCat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def randomcat(self, ctx, Num=None):
        if Num is None:
            await ctx.send('https://cataas.com/cat?' + str(randint(0, 10**6)))
        else:
            Num = int(Num)
            if Num > 2:
                await ctx.send("Превышено максимальное количество ссылок")
            else:
                for i in range(0, Num):
                    await ctx.send('https://cataas.com/cat?' + str(randint(0, 10**6)))


def setup(bot):
    bot.add_cog(randomCat(bot))
