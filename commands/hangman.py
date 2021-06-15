from commands.resources.hangman.Hangman import Hangman
from discord.ext.commands import Cog, group, guild_only
import asyncio
from discord.ext.commands.errors import NoPrivateMessage


class GameHangman(Cog):
    games = {}

    def __init__(self, bot):
        self.bot = bot

    # async def cog_command_error(self, ctx, error):
     #   if isinstance(error, NoPrivateMessage):
      #      await ctx.send('Игра только на серверах')

    @guild_only()
    @group(name='hangman', description='игра виселица', invoke_without_command=True)
    async def gameHangman(self, ctx):
        if ctx.message.author.bot:
            return
        if str(ctx.guild.id) in self.games:
            await ctx.send('Игра идет')
            return

        self.games[str(ctx.guild.id)] = [
            f'{ctx.author.id}',
            {'start': False}
        ]

        while str(ctx.guild.id) in self.games:
            await ctx.send(f'Игра начнется через 10с, игрок {ctx.author.mention}\nb/hangman stop для останвоки')
            await asyncio.sleep(10)

            if not (str(ctx.guild.id) in self.games):
                break

            if len(self.games[str(ctx.guild.id)][0]) == 0:
                self.games.pop(str(ctx.guild.id))
                return

            self.games[str(ctx.guild.id)][1] = True
            hangman = Hangman(ctx, ctx.author.id)
            await hangman.play()
            self.games[str(ctx.guild.id)][1] = False

    @guild_only()
    @gameHangman.command(name='stop', description='Остановить виселицу')
    async def stop(self, ctx):
        if ctx.message.author.bot:
            return
        if not str(ctx.guild.id) in self.games:
            return
        if self.games[str(ctx.guild.id)][1] == True:
            return

        await ctx.send('Игра остановлена')
        self.games.pop(str(ctx.guild.id))


def setup(bot):
    bot.add_cog(GameHangman(bot))
