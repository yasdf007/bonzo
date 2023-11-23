from discord.ext.commands.core import guild_only
from commands.resources.hangman.Hangman import Hangman
from discord.ext.commands import Cog, hybrid_group, Context
import asyncio
from bot import Bot


class GameHangman(Cog):
    games = {}

    def __init__(self, bot):
        self.bot: Bot = bot

    @hybrid_group(
        name="hangman", description="Начать игру виселица", invoke_without_command=True
    )
    @guild_only()
    async def gameHangman(self, ctx: Context):
        if ctx.author.bot:
            return

        guild_id = ctx.guild.id

        if str(guild_id) in self.games:
            await ctx.send("Игра идет")
            return

        self.games[str(guild_id)] = [
            f"{ctx.author.id}",
            {"started": False},
            {"end": False},
        ]

        while (
            str(guild_id) in self.games and self.games[str(guild_id)][2]["end"] == False
        ):
            await ctx.send(
                f"Игра начнется через 10с, игрок {ctx.author}\n/hangman stop для остановки"
            )
            await asyncio.sleep(10)

            if not (str(guild_id) in self.games):
                break

            if self.games[str(guild_id)][2]["end"] == True:
                self.games.pop(str(guild_id))
                return

            self.games[str(guild_id)][1] = True
            hangman = Hangman(ctx, ctx.author.id)
            isAfk = await hangman.play()

            if str(guild_id) in self.games:
                self.games[str(guild_id)][1] = False

            if isAfk == True:
                self.games.pop(str(guild_id))

    @gameHangman.command(
        name="start", description="Начать игру виселица", invoke_without_command=True
    )
    @guild_only()
    async def start(self, ctx: Context):
        await ctx.invoke(self.gameHangman)

    @gameHangman.command(name="stop", description="Остановить игру виселица")
    @guild_only()
    async def stop(self, ctx: Context):
        if ctx.author.bot:
            return

        guild_id = ctx.guild.id

        if not str(guild_id) in self.games:
            await ctx.send("Игра не идет")
            return

        if str(ctx.author.id) != self.games[str(guild_id)][0]:
            await ctx.send("Игру может остановить только тот, кто ее начал")
            return

        if self.games[str(guild_id)][1] == True:
            await ctx.send("Игра будет остановлена после текущей игры")
            self.games[str(guild_id)][2]["end"] = True
            return

        self.games[str(guild_id)][2]["end"] = True
        await ctx.send("Игра остановлена")


async def setup(bot):
    # TODO: FIX
    if False:
        await bot.add_cog(GameHangman(bot))
