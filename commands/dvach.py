from discord.ext.commands import Cog, CommandOnCooldown, command, cooldown
import requests
from random import choice
import json
name = '2ch'
description = 'Рандомное видео с двача'


class Dvach(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.USERAGENT = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        self.URL = 'https://api.randomtube.xyz/video.get'

    async def cog_command_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            await ctx.message.reply(error)

    @cooldown(rate=2, per=13)
    @command(name=name, description=description)
    async def dvach(self, ctx):
        res = requests.get(self.URL, headers=self.USERAGENT,
                           params={'board': 'b'})
        resJson = json.loads(res.text)
        link = choice(resJson['response']['items'])['url']
        await ctx.message.reply(link)


def setup(bot):
    bot.add_cog(Dvach(bot))
