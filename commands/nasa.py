from discord import Embed
from discord.ext.commands import Cog, CommandError, hybrid_command, Context
from .resources.AutomatedMessages import automata
from dependencies.api.nasa.abc import NasaAPI 
from bot import Bot

name = "nasapict"
description = "Картинка дня от NASA"


class NoPhotoFound(CommandError):
    pass


class Nasa(Cog):
    def __init__(self, bot):
        self.bot: Bot = bot
        self.nasa_api: NasaAPI = self.bot.dependency.nasa_api

    async def cog_command_error(self, ctx: Context, error):
        if isinstance(error, NoPhotoFound):
            return await ctx.send(
                automata.generateEmbErr("Не удалось получить картинку дня", error=error)
            )


    @hybrid_command(name=name, description=description)
    async def nasapict(self, ctx: Context):
        embed = Embed(title="Картинка дня от NASA", color=0x0000FF)
        try:    
            resp = await self.nasa_api.get_response()

            embed.set_image(url=resp.image)
            embed.set_footer(text=resp.title)

            await ctx.send(embed=embed)
        except Exception as e:
            raise NoPhotoFound


async def setup(bot):
    await bot.add_cog(Nasa(bot))
