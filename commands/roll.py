from discord import Embed
from discord.ext.commands.context import Context
from discord.ext.commands import Cog, command, CommandError
from discord_slash.error import SlashCommandError
from discord_slash import SlashContext, cog_ext
from random import randint
from typing import Optional
from config import guilds
from .resources.AutomatedMessages import automata

name = "roll"
description = "Ролит как в доте или между двумя числами"


class NumberTooLarge(CommandError, SlashCommandError):
    pass


class Roll(Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_command_error(self, ctx, error):
        if isinstance(error, NumberTooLarge):
            return await ctx.send(
                embed=automata.generateEmbErr(
                    "Числа больше 10^6 (миллион) не поддерживаются"
                )
            )

    @Cog.listener()
    async def on_slash_command_error(self, ctx, error):
        if isinstance(error, NumberTooLarge):
            return await ctx.send(
                embed=automata.generateEmbErr(
                    "Числа больше 10^6 (миллион) не поддерживаются"
                )
            )

    @command(name=name, description=description)
    async def roll_prefix(
        self,
        ctx: Context,
        number_from: Optional[int] = 100,
        *,
        number_to: Optional[int],
    ):
        await self.roll(ctx, number_from, number_to)

    @cog_ext.cog_slash(name=name, description=description)
    async def roll_slash(self, ctx: SlashContext, number_from: int, number_to: int):
        await self.roll(ctx, number_from, number_to)

    # dota 2 roll

    async def roll(self, ctx, number_from: int, number_to: int):
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


def setup(bot):
    bot.add_cog(Roll(bot))
