from commands.resources.AutomatedMessages import automata
from discord.ext.commands import Cog, command, CommandError, Context, hybrid_command
from aiohttp import ClientSession
from random import choice

name = "2ch"
description = "Рандомное видео с двача"


class RequestNetworkError(CommandError):
    pass


class Dvach(Cog):
    USERAGENT = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    URL = "https://api.randomtube.xyz/v1/videos"
    PARAMS = {"board": "b", "chan": "2ch.hk", "page": 1}

    def __init__(self, bot):
        self.bot = bot

    async def cog_command_error(self, ctx, error):
        if isinstance(error, RequestNetworkError):
            return await ctx.send(embed=automata.generateEmbErr("Ошибка при запросе"))

    @hybrid_command(name=name, description=description)
    async def dvach(self, ctx):
        async with ClientSession(headers=self.USERAGENT) as session:
            async with session.get(self.URL, params=self.PARAMS) as response:
                res = await response.json()

        try:
            link = choice(res["items"])["url"]
            await ctx.send(link)
        except:
            raise RequestNetworkError


async def setup(bot):
    await bot.add_cog(Dvach(bot))
