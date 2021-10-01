from commands.resources.AutomatedMessages import automata
from discord.ext.commands import Cog, command, CommandError, Context
from aiohttp import ClientSession
from random import choice
from discord_slash import SlashContext, cog_ext
from discord_slash.error import SlashCommandError
from config import guilds

name = '2ch'
description = 'Рандомное видео с двача'


class RequestNetworkError(CommandError, SlashCommandError):
    pass


class Dvach(Cog):
    USERAGENT = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }
    URL = 'https://api.randomtube.xyz/video.get'
    PARAMS = {'board': 'b'}

    def __init__(self, bot):
        self.bot = bot

    async def cog_command_error(self, ctx, error):
        if isinstance(error, RequestNetworkError):
            return await ctx.send(embed=automata.generateEmbErr('Ошибка при запросе'))

    @Cog.listener()
    async def on_slash_command_error(self, ctx, error):
        if isinstance(error, RequestNetworkError):
            return await ctx.send(embed=automata.generateEmbErr('Ошибка при запросе'))

    @command(name=name, description=description)
    async def dvach_prefix(self, ctx: Context):
        await self.dvach(ctx)

    @cog_ext.cog_slash(name=name, description=description)
    async def dvach_slash(self, ctx: SlashContext):
        await self.dvach(ctx)

    async def dvach(self, ctx):
        async with ClientSession(headers=self.USERAGENT) as session:
            async with session.get(self.URL, params=self.PARAMS) as response:
                res = await response.json()
        try:
            link = choice(res['response']['items'])['url']
            await ctx.send(link)
        except:
            raise RequestNetworkError


def setup(bot):
    bot.add_cog(Dvach(bot))
