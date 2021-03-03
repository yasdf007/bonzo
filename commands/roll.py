from discord.ext.commands import Cog, CommandInvokeError, CommandOnCooldown, cooldown, command, BucketType
from random import randint
from discord import Embed
from typing import Optional

name = 'roll'
description = 'Ролит как в доте или между двумя числами (Будет переписан)'


class roll(Cog):
    def __init__(self, bot):
        self.bot = bot

    # Обработка ошибок
    async def cog_command_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            await ctx.message.reply(error)
        if isinstance(error, CommandInvokeError):
            await ctx.message.reply(error.original)

    # dota 2 roll
    @cooldown(rate=1, per=3, type=BucketType.user)
    @command(name=name, description=description)
    async def roll(self, ctx, numberFrom: Optional[int] = 100, *, numberTo: Optional[int]):
        oneMillon = 10**6

        try:
            # Чекаем на значение, если больше ляма..
            assert numberFrom <= oneMillon if numberFrom else 1
            assert numberTo <= oneMillon if numberTo else 1

        except AssertionError:
            # То ошибка
            raise CommandInvokeError(
                f'{ctx.author.mention} больше мильёна роллить не буду')
        embed = Embed()
        # Еслм два числа указаны
        if numberFrom and numberTo:
            # Если первое число больше второго
            if numberFrom > numberTo:
                # Меняем местами
                numberFrom, numberTo = numberTo, numberFrom

            embed.title = f'Rolling from {numberFrom} to {numberTo}:'
            embed.add_field(name='Number Is',
                            value=f'{randint(numberFrom, numberTo)}', inline=False)
            await ctx.message.reply(embed=embed)
            return

        # Если указано одно
        if numberFrom and not numberTo:
            embed.title = f'Rolling from 1 to {numberFrom}:'
            embed.add_field(name='Number Is',
                            value=f'{randint(1, numberFrom)}', inline=False)
            await ctx.message.reply(embed=embed)
            return


def setup(bot):
    bot.add_cog(roll(bot))
