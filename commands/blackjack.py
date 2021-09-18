from discord.ext.commands import Cog, group, guild_only
import asyncio
from discord.ext.commands.errors import NoPrivateMessage
from .resources.blackjack.Blackjack import Blackjack
from discord_slash import SlashContext, cog_ext
from config import guilds


class gameBlackjack(Cog):
    games = {}

    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_subcommand(base='blackjack', name='start', description='Начать игру blackjack')
    async def gameBlackjack(self, ctx):
        if ctx.author.bot:
            return

        if str(ctx.guild.id) in self.games:
            await ctx.send('Игра идет')
            return

        self.games[str(ctx.guild.id)] = [
            [f'{ctx.author.id}'],
            {'start': False}
        ]

        while str(ctx.guild.id) in self.games:
            await ctx.send('Ждем игроков 15 секунд, `/blackjack join` для входа в игру')
            await asyncio.sleep(5)

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

    @cog_ext.cog_subcommand(base='blackjack', name='join', description='Присоединиться к игре blackjack')
    async def join(self, ctx):
        if ctx.author.bot:
            return

        if not str(ctx.guild.id) in self.games:
            await ctx.send(f'Игра не идет')
            return

        if self.games[str(ctx.guild.id)][1] == True:
            await ctx.send(f'Игра идет')
            return

        if str(ctx.author.id) in (self.games[str(ctx.guild.id)][0]):
            await ctx.send(f'Уже в игре')
            return

        self.games[str(ctx.guild.id)][0].append(str(ctx.author.id))
        await ctx.send(f'Добавил {ctx.message.author}')

    @cog_ext.cog_subcommand(base='blackjack', name='stop', description='Остановить blackjack')
    async def stop(self, ctx):
        if ctx.author.bot:
            return

        if not str(ctx.guild.id) in self.games:
            await ctx.send(f'Игра не идет')
            return

        if self.games[str(ctx.guild.id)][1] == True:
            await ctx.send(f'Игра идет')
            return

        self.games.pop(str(ctx.guild.id))
        await ctx.send('Игра остановлена')

    @cog_ext.cog_subcommand(base='blackjack', name='leave', description='Выйти из blackjack')
    async def leave(self, ctx):
        if ctx.author.bot:
            return

        if not str(ctx.guild.id) in self.games:
            await ctx.send(f'Игра не идет')
            return

        if not str(ctx.author.id) in self.games[str(ctx.guild.id)][0]:
            await ctx.send(f'Ты не в игре')
            return

        if self.games[str(ctx.guild.id)][1] == True:
            await ctx.send(f'Игра идет')
            return

        if str(ctx.author.id) in (self.games[str(ctx.guild.id)][0]):
            self.games[str(ctx.guild.id)][0].remove(str(ctx.author.id))
            await ctx.send(f'Удалил {ctx.author}')


def setup(bot):
    bot.add_cog(gameBlackjack(bot))
