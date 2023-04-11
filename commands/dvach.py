from discord.ext.commands import Cog, Context, hybrid_command

from dependencies.api.dvach.abc import DvachAPI
from bot import Bot
from .resources.exceptions import CustomCheckError

name = "2ch"
description = "Рандомное видео с двача"


class Dvach(Cog):
    def __init__(self, bot):
        self.bot: Bot = bot
        self.dvach_api: DvachAPI = self.bot.dependency.dvach_api

    @hybrid_command(name=name, description=description)
    async def dvach(self, ctx: Context):
        try:
            link = await self.dvach_api.get_random_url()
            await ctx.send(link)
        except:
            raise CustomCheckError(message="Ошибка при запросе")

async def setup(bot):
    await bot.add_cog(Dvach(bot))
