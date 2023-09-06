from discord.ext.commands import Cog, Context, hybrid_command

from bot import Bot
from .resources.exceptions import CustomCheckError

from dependencies.api import dvach

name = "2ch"
description = "Рандомное видео с двача"


class Dvach(Cog):
    def __init__(self, bot, random_tube: dvach.RandomtubeAPI):
        self.bot: Bot = bot
        self.random_tube = random_tube

    @hybrid_command(name=name, description=description)
    async def dvach(self, ctx: Context):
        try:
            link = await self.random_tube.get_random_url()
            await ctx.send(link)
        except:
            raise CustomCheckError(message="Ошибка при запросе")

async def setup(bot):
    random_tube = dvach.RandomtubeAPI()
    await bot.add_cog(Dvach(bot, random_tube))
