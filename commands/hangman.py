from discord.ext.commands.core import group, guild_only
from discord_slash.context import SlashContext
from commands.resources.hangman.Hangman import Hangman
from discord.ext.commands import Cog, command, group
from discord.ext.commands.context import Context
import asyncio
from discord_slash import SlashContext, cog_ext
from config import guilds


class GameHangman(Cog):
    games = {}

    def __init__(self, bot):
        self.bot = bot

    @guild_only()
    @group(name='hangman', description='Начать игру виселица', invoke_without_command=True)
    async def gameHangman_prefix(self, ctx: Context):
        await self.gameHangman(ctx)

    @cog_ext.cog_subcommand(base='hangman', name='start', description='Начать игру виселица')
    async def gameHangman_slash(self, ctx: SlashContext):
        await self.gameHangman(ctx)

    async def gameHangman(self, ctx):
        if ctx.author.bot:
            return

        if isinstance(ctx, Context):
            guild_id = ctx.guild.id
        if isinstance(ctx, SlashContext):
            guild_id = ctx.guild_id

        if str(guild_id) in self.games:
            await ctx.send('Игра идет')
            return

        self.games[str(guild_id)] = [
            f'{ctx.author.id}',
            {'started': False},
            {'end': False}
        ]

        while str(guild_id) in self.games and self.games[str(guild_id)][2]['end'] == False:
            await ctx.send(f'Игра начнется через 10с, игрок {ctx.author}\n/hangman stop для остановки')
            await asyncio.sleep(10)

            if not (str(guild_id) in self.games):
                break

            if self.games[str(guild_id)][2]['end'] == True:
                self.games.pop(str(guild_id))
                return

            self.games[str(guild_id)][1] = True
            hangman = Hangman(ctx, ctx.author.id)
            isAfk = await hangman.play()

            if str(guild_id) in self.games:
                self.games[str(guild_id)][1] = False

            if isAfk == True:
                self.games.pop(str(guild_id))

    @guild_only()
    @gameHangman_prefix.command(name='stop', description='Остановить игру виселица')
    async def stop_prefix_(self, ctx: Context):
        await self.stop(ctx)

    @cog_ext.cog_subcommand(base='hangman', name='stop', description='Остановить игру виселица')
    async def stop_slash_(self, ctx: SlashContext):
        await self.stop(ctx)

    async def stop(self, ctx):
        if ctx.author.bot:
            return

        if isinstance(ctx, Context):
            guild_id = ctx.guild.id
        if isinstance(ctx, SlashContext):
            guild_id = ctx.guild_id

        if not str(guild_id) in self.games:
            await ctx.send('Игра не идет')
            return

        if str(ctx.author.id) != self.games[str(guild_id)][0]:
            await ctx.send('Игру может остановить только тот, кто ее начал')
            return

        if self.games[str(guild_id)][1] == True:
            await ctx.send('Игра будет остановлена после текущей игры')
            self.games[str(guild_id)][2]['end'] = True
            return

        self.games[str(guild_id)][2]['end'] = True
        await ctx.send('Игра остановлена')


def setup(bot):
    bot.add_cog(GameHangman(bot))
