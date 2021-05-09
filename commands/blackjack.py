from discord.ext.commands import Cog, command, group
from discord import Embed
import asyncio
from .resources.blackjack.Blackjack import Blackjack


class gameBlackjack(Cog):
    games = {}

    def __init__(self, bot):
        self.bot = bot

    @group(name='blackjack', description='игра blackjack (21)')
    async def gameBlackjack(self, ctx):
        if ctx.invoked_subcommand:
            return

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

    @gameBlackjack.command(name='join', desciption='Присоедениться к игре blackjack')
    async def join(self, ctx):
        if not str(ctx.guild.id) in self.games:
            return

        if not str(ctx.message.author.id) in self.games[str(ctx.guild.id)] and not ctx.message.author.bot:
            self.games[str(ctx.guild.id)].append(str(ctx.message.author.id))
            await ctx.reply(f'Добавил {ctx.message.author}')


def setup(bot):
    bot.add_cog(gameBlackjack(bot))
