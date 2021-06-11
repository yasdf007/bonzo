from discord.ext.commands import Cog, group, guild_only
import asyncio
from discord.ext.commands.errors import NoPrivateMessage
from .resources.blackjack.Blackjack import Blackjack


class gameBlackjack(Cog):
    games = {}

    def __init__(self, bot):
        self.bot = bot

    async def cog_command_error(self, ctx, error):
        if isinstance(error, NoPrivateMessage):
            await ctx.send('Игра только на серверах')

    @guild_only()
    @group(name='blackjack', description='игра blackjack (21)', invoke_without_command=True)
    async def gameBlackjack(self, ctx):
        if str(ctx.guild.id) in self.games:
            await ctx.send('Игра идет')
            return

        self.games[str(ctx.guild.id)] = [
            [f'{ctx.author.id}'],
            {'start': False}
        ]

        while str(ctx.guild.id) in self.games:
            await ctx.send('Ждем игроков 15 секунд, `b/blackjack join` для входа в игру')
            await asyncio.sleep(15)

            if not (str(ctx.guild.id) in self.games):
                break

            if len(self.games[str(ctx.guild.id)][0]) == 0:
                self.games.pop(str(ctx.guild.id))
                return

            self.games[str(ctx.guild.id)][1] = True
            blackjack = Blackjack(
                ctx, players=self.games[str(ctx.guild.id)][0])
            await blackjack.play()

            self.games[str(ctx.guild.id)][1] = False

    @guild_only()
    @gameBlackjack.command(name='join', description='Присоединиться к игре blackjack')
    async def join(self, ctx):
        if not str(ctx.guild.id) in self.games:
            return
        if self.games[str(ctx.guild.id)][1] == True:
            return
        if not str(ctx.message.author.id) in (self.games[str(ctx.guild.id)][0]) and not ctx.message.author.bot:
            self.games[str(ctx.guild.id)][0].append(str(ctx.message.author.id))
            await ctx.reply(f'Добавил {ctx.message.author}')

    @guild_only()
    @gameBlackjack.command(name='stop', description='Остановить blackjack')
    async def stop(self, ctx):
        if not str(ctx.guild.id) in self.games:
            return
        if self.games[str(ctx.guild.id)][1] == True:
            return
        if ctx.message.author.bot:
            return

        await ctx.send('Игра остановлена')
        self.games.pop(str(ctx.guild.id))

    @guild_only()
    @gameBlackjack.command(name='leave', description='Выйти из blackjack')
    async def leave(self, ctx):
        if not str(ctx.guild.id) in self.games:
            return
        if not str(ctx.author.id) in self.games[str(ctx.guild.id)][0]:
            return

        if str(ctx.message.author.id) in (self.games[str(ctx.guild.id)][0]) and not ctx.message.author.bot:
            self.games[str(ctx.guild.id)][0].remove(str(ctx.message.author.id))
            await ctx.reply(f'Удалил {ctx.message.author}')


def setup(bot):
    bot.add_cog(gameBlackjack(bot))
