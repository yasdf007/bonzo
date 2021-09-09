from discord.ext.commands import Cog
from aiohttp import ClientSession
from random import choice
from discord_slash import SlashContext, cog_ext
from config import guilds

name = '2ch'
description = 'Рандомное видео с двача'


class Dvach(Cog):
    USERAGENT = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }
    URL = 'https://api.randomtube.xyz/video.get'
    PARAMS = {'board': 'b'}

    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name=name, description=description, guild_ids=guilds)
    async def dvach(self, ctx: SlashContext):
        async with ClientSession(headers=self.USERAGENT) as session:
            async with session.get(self.URL, params=self.PARAMS) as response:
                res = await response.json()

        link = choice(res['response']['items'])['url']
        await ctx.send(link)


def setup(bot):
    bot.add_cog(Dvach(bot))
