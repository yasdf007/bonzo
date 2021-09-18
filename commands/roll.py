from discord.ext.commands import Cog
from random import randint
from discord import Embed
from discord_slash import SlashContext, cog_ext
from config import guilds

name = 'roll'
description = 'Ролит как в доте или между двумя числами'


class Roll(Cog):
    def __init__(self, bot):
        self.bot = bot

    # dota 2 roll
    @cog_ext.cog_slash(name=name, description=description)
    async def roll(self, ctx: SlashContext, number_from: int,  number_to: int):
        oneMillon = 10**6

        try:
            # Чекаем на значение, если больше ляма..
            assert number_from <= oneMillon if number_from else 1
            assert number_to <= oneMillon if number_to else 1

        except AssertionError:
            # То ошибка
            await ctx.send(
                f'{ctx.author.mention} больше мильёна роллить не буду')
            return

        embed = Embed()
        # Еслм два числа указаны
        if number_from and number_to:
            # Если первое число больше второго
            if number_from > number_to:
                # Меняем местами
                number_from, number_to = number_to, number_from

            embed.title = f'Rolling from {number_from} to {number_to}:'
            embed.add_field(name='Number Is',
                            value=f'{randint(number_from, number_to)}', inline=False)
            await ctx.send(embed=embed)
            return

        # Если указано одно
        if number_from and not number_to:
            embed.title = f'Rolling from 1 to {number_from}:'
            embed.add_field(name='Number Is',
                            value=f'{randint(1, number_from)}', inline=False)
            await ctx.send(embed=embed)
            return


def setup(bot):
    bot.add_cog(Roll(bot))
