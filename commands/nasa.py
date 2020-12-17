from discord import Embed
from discord.ext.commands import Cog, command
from requests import get
import json

name = 'nasapict'
description = 'Картинка дня от NASA'


class Nasa(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name=name, description=description)
    async def nasapict(self, ctx):
        embed = Embed(title='Картинка дня от NASA', color=0x0000ff)

        query = 'https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY'
        res = get(query)
        resJson = json.loads(res.text)

        embed.set_image(url=resJson['hdurl'])
        embed.set_footer(text=resJson['title'])

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Nasa(bot))
