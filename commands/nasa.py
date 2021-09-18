from discord import Embed
from discord.ext.commands import Cog
from aiohttp import ClientSession
from discord_slash import SlashContext, cog_ext
from config import guilds

name = 'nasapict'
description = 'Картинка дня от NASA'


class Nasa(Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name=name, description=description, guild_ids=guilds)
    async def nasapict(self, ctx: SlashContext):
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
