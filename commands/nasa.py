from discord import Embed
from discord.ext.commands.context import Context
from discord.ext.commands import Cog, command, CommandError, hybrid_command
from aiohttp import ClientSession
from .resources.AutomatedMessages import automata

name = "nasapict"
description = "Картинка дня от NASA"


class NoPhotoFound(CommandError):
    pass


class Nasa(Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_command_error(self, ctx, error):
        if isinstance(error, NoPhotoFound):
            return await ctx.send(
                automata.generateEmbErr("Не удалось получить картинку дня", error=error)
            )


    @hybrid_command(name=name, description=description)
    async def nasapict(self, ctx):
        embed = Embed(title="Картинка дня от NASA", color=0x0000FF)

        query = "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY"
        async with ClientSession() as session:
            async with session.get(query) as response:
                res = await response.json()
        try:
            image = res["hdurl"]
            title = res["title"]

            embed.set_image(url=image)
            embed.set_footer(text=title)

            await ctx.send(embed=embed)
        except Exception as e:
            raise NoPhotoFound


async def setup(bot):
    await bot.add_cog(Nasa(bot))
