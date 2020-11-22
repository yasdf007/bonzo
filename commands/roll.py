from discord.ext import commands
from random import randint

name='roll'
description='Ролит как в доте или между двумя числами (Будет переписан)'

class roll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Обработка ошибок
    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send('Нужно ввести число до миллиона')

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(error)

    # dota 2 roll
    @commands.cooldown(rate=1, per=3)
    @commands.command(name=name, description=description)
    async def roll(self, ctx, a=None, b=None):
        # Если оба числа не указаны
        if a is None and b is None:
            # Ролим от 1 до 100
            await ctx.send('{0.author.mention}'.format(ctx) + ' Random Number is: ' + str(randint(1, 100)))

        # Если одна из границ не указана
        elif b is None:
            # Ролим от 1 до того числа, который был указан
            a = int(a)
            if a <= 10**6:
                await ctx.send('{0.author.mention}'.format(ctx) + ' Random Number is: ' + str(randint(1, a)))
            else:
                # Если число больше миллиона, отправляем ошибку
                raise commands.CommandInvokeError()
        else:
            # Роляем по границам
            a, b = int(a), int(b)
            if b <= 10**6:
                await ctx.send('{0.author.mention}'.format(ctx) + ' Random Number is: ' + str(randint(a, b)))
            else:
                await ctx.send('{0.author.mention}'.format(ctx) + ' больше мильёна роллить не буду')


def setup(bot):
    bot.add_cog(roll(bot))
