from discord import Embed
from discord.ext.commands import Cog, command
from discord.ext.commands.context import Context
from aiohttp import ClientSession
from discord_slash import SlashContext, cog_ext
from config import guilds

name = 'nasapict'
description = 'Картинка дня от NASA'


class Nasa(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name=name, description=description)
    async def nasapict_prefix(self, ctx: Context):
        await self.nasapict(ctx)

    @cog_ext.cog_slash(name=name, description=description)
    async def nasapict_slash(self, ctx: SlashContext):
        await self.nasapict(ctx)

    async def nasapict(self, ctx):
        embed = Embed(title='Картинка дня от NASA', color=0x0000ff)

        query = 'https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY'
        async with ClientSession() as session:
            async with session.get(query) as response:
                res = await response.json()
        try:
            image = res['hdurl']
            title = res['title']

            embed.set_image(url=image)
            embed.set_footer(text=title)

            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send('Не удалось получить картинку дня')


def setup(bot):
    bot.add_cog(Nasa(bot))
