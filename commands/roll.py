from discord import Embed
from discord.ext.commands import Cog, CommandError, hybrid_command, Context
from random import randint
from .resources.AutomatedMessages import automata
from bot import Bot

name = "roll"
description = "Ролит как в доте или между двумя числами"


class NumberTooLarge(CommandError):
    pass


class Roll(Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    async def cog_command_error(self, ctx: Context, error):
        if isinstance(error, NumberTooLarge):
            return await ctx.send(
                embed=automata.generateEmbErr(
                    "Числа больше 10^6 (миллион) не поддерживаются"
                )
            )
        raise error


    # dota 2 roll

    @hybrid_command(name=name, description=description)
    async def roll(self, ctx: Context, number_from: int = 1, number_to: int = 100):
        oneMillon = 10 ** 6

        try:
            # Чекаем на значение, если больше ляма..
            assert number_from <= oneMillon if number_from else 1
            assert number_to <= oneMillon if number_to else 1

        except AssertionError:
            # То ошибка
            raise NumberTooLarge

        embed = Embed()
        # Еслм два числа указаны
        if number_from and number_to:
            # Если первое число больше второго
            if number_from > number_to:
                # Меняем местами
                number_from, number_to = number_to, number_from

            embed.title = f"Rolling from {number_from} to {number_to}:"
            embed.add_field(
                name="Number Is",
                value=f"{randint(number_from, number_to)}",
                inline=False,
            )
            await ctx.send(embed=embed)
            return

        # Если указано одно
        if number_from and not number_to:
            embed.title = f"Rolling from 1 to {number_from}:"
            embed.add_field(
                name="Number Is", value=f"{randint(1, number_from)}", inline=False
            )
            await ctx.send(embed=embed)
            return


async def setup(bot):
    await bot.add_cog(Roll(bot))
