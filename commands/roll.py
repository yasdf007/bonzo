from discord.ext.commands import Cog, CommandInvokeError, CommandOnCooldown, cooldown, command
from random import randint

name = 'roll'
description = 'Ролит как в доте или между двумя числами (Будет переписан)'


class roll(Cog):
    def __init__(self, bot):
        self.bot = bot

    # Обработка ошибок
    async def cog_command_error(self, ctx, error):
        if isinstance(error, CommandInvokeError):
            await ctx.send('Нужно ввести число до миллиона')

    async def cog_command_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            await ctx.send(error)

    # dota 2 roll
    @cooldown(rate=1, per=3)
    @command(name=name, description=description)
    async def roll(self, ctx, numberFrom=None, numberTo=None):
        # Если оба числа не указаны
        if numberFrom is None and numberTo is None:
            # Ролим от 1 до 100
            await ctx.send('{0.author.mention}'.format(ctx) + ' Random Number is: ' + str(randint(1, 100)))

        # Если одна из границ не указана
        elif numberTo is None:
            # Ролим от 1 до того числа, который был указан
            numberFrom = int(numberFrom)
            if numberFrom <= 10**6:
                await ctx.send('{0.author.mention}'.format(ctx) + ' Random Number is: ' + str(randint(1, numberFrom)))
            else:
                # Если число больше миллиона, отправляем ошибку
                raise CommandInvokeError()
        else:
            # Роляем по границам
            numberFrom, numberTo = int(numberFrom), int(numberTo)
            if numberTo <= 10**6:
                await ctx.send('{0.author.mention}'.format(ctx) + ' Random Number is: ' + str(randint(numberFrom, numberTo)))
            else:
                await ctx.send('{0.author.mention}'.format(ctx) + ' больше мильёна роллить не буду')


def setup(bot):
    bot.add_cog(roll(bot))
