from discord import Embed
from discord.ext.commands import Cog, hybrid_command, Context
from dependencies.api.nasa.abc import NasaAPI 
from bot import Bot
from .resources.exceptions import CustomCheckError
name = "nasapict"
description = "Картинка дня от NASA"


class Nasa(Cog):
    def __init__(self, bot):
        self.bot: Bot = bot
        self.nasa_api: NasaAPI = self.bot.dependency.nasa_api

    @hybrid_command(name=name, description=description)
    async def nasapict(self, ctx: Context):
        embed = Embed(title="Картинка дня от NASA", color=0x0000FF)
        try:    
            resp = await self.nasa_api.get_response()

            embed.set_image(url=resp.image)
            embed.set_footer(text=resp.title)

            await ctx.send(embed=embed)
        except Exception as e:
            raise CustomCheckError(message="Не удалось получить картинку дня")


async def setup(bot):
    await bot.add_cog(Nasa(bot))
