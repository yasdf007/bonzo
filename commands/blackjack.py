from discord.ext.commands import Cog, guild_only, hybrid_group, Context
from discord.ext.commands.errors import NoPrivateMessage

from .resources.blackjack.Blackjack import Blackjack
from .resources.AutomatedMessages import automata

from bot import Bot

import asyncio

class gameBlackjack(Cog):
    games = {}

    def __init__(self, bot):
        self.bot: Bot = bot

    async def cog_command_error(self, ctx: Context, error):
        if isinstance(error, NoPrivateMessage):
            return await ctx.send(
                embed=automata.generateEmbErr(
                    "Эту команду нельзя использовать в ЛС.", error=error
                )
            )

        await ctx.send("Произошла ошибка во время игры.")
        self.games.pop(str(ctx.guild.id))
        raise error

    @hybrid_group(
        name="blackjack",
        description="Начать игру blackjack",
        invoke_without_command=True,
    )
    @guild_only()
    async def gameBlackjack(self, ctx: Context):
        if ctx.author.bot:
            return

        if str(ctx.guild.id) in self.games:
            await ctx.send("Игра идет")
            return

        self.games[str(ctx.guild.id)] = [[f"{ctx.author.id}"], {"start": False}]

        while str(ctx.guild.id) in self.games:
            await ctx.send("Ждем игроков 15 секунд, `/blackjack join` для входа в игру")
            await asyncio.sleep(5)

            if not (str(ctx.guild.id) in self.games):
                break

            if len(self.games[str(ctx.guild.id)][0]) == 0:
                self.games.pop(str(ctx.guild.id))
                return

            self.games[str(ctx.guild.id)][1] = True
            blackjack = Blackjack(ctx, players=self.games[str(ctx.guild.id)][0])
            await blackjack.play()

            self.games[str(ctx.guild.id)][1] = False

    @gameBlackjack.command(name="join", description="Присоединиться к игре blackjack")
    @guild_only()
    async def join(self, ctx: Context):
        if ctx.author.bot:
            return

        if not str(ctx.guild.id) in self.games:
            await ctx.send(f"Игра не идет")
            return

        if self.games[str(ctx.guild.id)][1] == True:
            await ctx.send(f"Игра идет")
            return

        if str(ctx.author.id) in (self.games[str(ctx.guild.id)][0]):
            await ctx.send(f"Уже в игре")
            return

        self.games[str(ctx.guild.id)][0].append(str(ctx.author.id))
        await ctx.send(f"Добавил {ctx.message.author}")

    @gameBlackjack.command(name="stop", description="Остановить blackjack")
    @guild_only()
    async def stop(self, ctx: Context):
        if ctx.author.bot:
            return

        if not str(ctx.guild.id) in self.games:
            await ctx.send(f"Игра не идет")
            return

        if self.games[str(ctx.guild.id)][1] == True:
            await ctx.send(f"Игра идет")
            return

        self.games.pop(str(ctx.guild.id))
        await ctx.send("Игра остановлена")

    @gameBlackjack.command(name="leave", description="Выйти из blackjack")
    async def leave(self, ctx: Context):
        if ctx.author.bot:
            return

        if not str(ctx.guild.id) in self.games:
            await ctx.send(f"Игра не идет")
            return

        if not str(ctx.author.id) in self.games[str(ctx.guild.id)][0]:
            await ctx.send(f"Ты не в игре")
            return

        if self.games[str(ctx.guild.id)][1] == True:
            await ctx.send(f"Игра идет")
            return

        if str(ctx.author.id) in (self.games[str(ctx.guild.id)][0]):
            self.games[str(ctx.guild.id)][0].remove(str(ctx.author.id))
            await ctx.send(f"Удалил {ctx.author}")


async def setup(bot):
    await bot.add_cog(gameBlackjack(bot))
