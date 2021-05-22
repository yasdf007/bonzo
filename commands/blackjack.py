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

        self.games[str(ctx.guild.id)] = []

        await ctx.send('Ждем игроков 15 секунд, bd/blackjack join для входа в игру')

        await asyncio.sleep(15)

        if len(self.games[str(ctx.guild.id)]) == 0:
            self.games.pop(str(ctx.guild.id))
            return

        blackjack = Blackjack(ctx, players=self.games[str(ctx.guild.id)])
        await blackjack.play()
        self.games.pop(str(ctx.guild.id))

    @guild_only()
    @gameBlackjack.command(name='join', description='Присоедениться к игре blackjack')
    async def join(self, ctx):
        if not str(ctx.guild.id) in self.games:
            return

        if not str(ctx.message.author.id) in self.games[str(ctx.guild.id)] and not ctx.message.author.bot:
            self.games[str(ctx.guild.id)].append(str(ctx.message.author.id))
            await ctx.reply(f'Добавил {ctx.message.author}')


def setup(bot):
    bot.add_cog(gameBlackjack(bot))
