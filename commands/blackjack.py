from discord.ext.commands import Cog, command, group
from discord import Embed
import asyncio
from .resources.blackjack.Blackjack import Blackjack


class gameBlackjack(Cog):
    gameStart = False

    def __init__(self, bot):
        self.bot = bot
        self.players = []

    @group(name='blackjack', description='игра blackjack (21)')
    async def gameBlackjack(self, ctx):
        if ctx.invoked_subcommand:
            return

        if self.gameStart == True:
            await ctx.send('Игра идет')
            return

        self.players = []

        self.gameStart = True

        await ctx.send('Ждем игроков 15 секунд, bd/blackjack join для входа в игру')

        await asyncio.sleep(15)

        if len(self.players) == 0:
            self.gameStart = False
            return

        print(self.players)

        blackjack = Blackjack(ctx, players=self.players)
        await blackjack.play()

        self.gameStart = False

    @gameBlackjack.command(name='join', desciption='Присоедениться к игре blackjack')
    async def join(self, ctx):
        if self.gameStart == False:
            return
        if not str(ctx.author.id) in self.players and not ctx.message.author.bot:
            self.players.append(str(ctx.message.author.id))
            await ctx.reply(f'Добавил {ctx.message.author}')


def setup(bot):
    bot.add_cog(gameBlackjack(bot))
