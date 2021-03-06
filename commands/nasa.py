from discord import Embed
from discord.ext.commands import Cog, command
from aiohttp import ClientSession

name = 'nasapict'
description = 'Картинка дня от NASA'


class Nasa(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name=name, description=description)
    async def nasapict(self, ctx):
        embed = Embed(title='Картинка дня от NASA', color=0x0000ff)

        query = 'https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY'
        async with ClientSession() as session:
            async with session.get(query) as response:
                res = await response.json()

        embed.set_image(url=res['hdurl'])
        embed.set_footer(text=res['title'])

        await ctx.message.reply(embed=embed)


def setup(bot):
    bot.add_cog(Nasa(bot))
