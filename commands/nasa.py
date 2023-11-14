from discord import Embed, Interaction, app_commands
from discord.ext.commands import Cog, hybrid_command, Context
from bot import Bot
from .resources.exceptions import CustomCheckError
from dependencies.api import nasa

class Nasa(Cog):
    def __init__(self, bot, nasa_api: nasa.NasaApi):
        self.bot: Bot = bot
        self.nasa_api = nasa_api

    @app_commands.command(name="nasapict", description="Картинка дня от NASA")
    async def nasapict(self, inter: Interaction):
        resp = await self.nasa_api.get_image_of_the_day()

        embed = Embed(title="Картинка дня от NASA", color=0x0000FF)
        embed.set_image(url=resp['image'])
        embed.set_footer(text=resp['title'])

        await inter.response.send_message(embed=embed)


async def setup(bot):
    nasa_api = nasa.NasaApi()
    await bot.add_cog(Nasa(bot, nasa_api))
