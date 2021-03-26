from discord.ext.commands import Cog, CommandOnCooldown, command, cooldown, BucketType
from aiohttp import ClientSession
from random import choice

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

    async def cog_command_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            await ctx.message.reply(error)

    @cooldown(rate=2, per=13, type=BucketType.user)
    @command(name=name, description=description)
    async def dvach(self, ctx):
        async with ClientSession(headers=self.USERAGENT) as session:
            async with session.get(self.URL, params=self.PARAMS) as response:
                res = await response.json()

        link = choice(res['response']['items'])['url']
        await ctx.message.reply(link)


def setup(bot):
    bot.add_cog(Dvach(bot))
