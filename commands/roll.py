from discord.ext import commands
from random import randint


class roll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # dota 2 roll
    @commands.command()
    async def roll(self, ctx, a=None, b=None):
        if a is None and b is None:
            await ctx.send('{0.author.mention}'.format(ctx) + ' Random Number is: ' + str(randint(1, 100)))
        elif b is None:
            a = int(a)
            if a <= 10**6:
                await ctx.send('{0.author.mention}'.format(ctx) + ' Random Number is: ' + str(randint(1, a)))
            else:
                await ctx.send('{0.author.mention}'.format(ctx) + ' больше мильёна роллить не буду')
        else:
            a, b = int(a), int(b)
            if b <= 10**6:
                await ctx.send('{0.author.mention}'.format(ctx) + ' Random Number is: ' + str(randint(a, b)))
            else:
                await ctx.send('{0.author.mention}'.format(ctx) + ' больше мильёна роллить не буду')


def setup(bot):
    bot.add_cog(roll(bot))
