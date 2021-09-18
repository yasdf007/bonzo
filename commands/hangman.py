from discord_slash.context import SlashContext
from commands.resources.hangman.Hangman import Hangman
from discord.ext.commands import Cog
import asyncio
from discord_slash import SlashContext, cog_ext
from config import guilds


class GameHangman(Cog):
    games = {}

    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_subcommand(base='hangman', name='start', description='Начать игру виселица')
    async def gameHangman(self, ctx):
        if ctx.author.bot:
            return

        if str(ctx.guild.id) in self.games:
            await ctx.send('Игра идет')
            return

        self.games[str(ctx.guild.id)] = [
            f'{ctx.author.id}',
            {'started': False},
            {'end': False}
        ]

        while str(ctx.guild.id) in self.games and self.games[str(ctx.guild.id)][2]['end'] == False:
            await ctx.send(f'Игра начнется через 10с, игрок {ctx.author}\n/hangman stop для остановки')
            await asyncio.sleep(10)

            if not (str(ctx.guild.id) in self.games):
                break

            if self.games[str(ctx.guild.id)][2]['end'] == True:
                self.games.pop(str(ctx.guild.id))
                return

            self.games[str(ctx.guild.id)][1] = True
            hangman = Hangman(ctx, ctx.author.id)
            isAfk = await hangman.play()

            if str(ctx.guild.id) in self.games:
                self.games[str(ctx.guild.id)][1] = False

            if isAfk == True:
                self.games.pop(str(ctx.guild.id))

    @cog_ext.cog_subcommand(base='hangman', name='stop', description='Остановить игру виселица')
    async def stop(self, ctx: SlashContext):
        if ctx.author.bot:
            return

        if not str(ctx.guild.id) in self.games:
            await ctx.send('Игра не идет')
            return

        if str(ctx.author.id) != self.games[str(ctx.guild.id)][0]:
            await ctx.send('Игру может остановить только тот, кто ее начал')
            return

        if self.games[str(ctx.guild.id)][1] == True:
            await ctx.send('Игра будет остановлена после текущей игры')
            self.games[str(ctx.guild.id)][2]['end'] = True
            return

        self.games[str(ctx.guild.id)][2]['end'] = True
        await ctx.send('Игра остановлена')


def setup(bot):
    bot.add_cog(GameHangman(bot))
