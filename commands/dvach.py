from commands.resources.AutomatedMessages import automata
from discord.ext.commands import Cog, CommandError, Context, hybrid_command

from dependencies.api.dvach.abc import DvachAPI
from bot import Bot

name = "2ch"
description = "Рандомное видео с двача"


class RequestNetworkError(CommandError):
    pass

class Dvach(Cog):
    def __init__(self, bot):
        self.bot: Bot = bot
        self.dvach_api: DvachAPI = self.bot.dependency.dvach_api

    async def cog_command_error(self, ctx: Context, error):
        if isinstance(error, RequestNetworkError):
            return await ctx.send(embed=automata.generateEmbErr("Ошибка при запросе"))

    @hybrid_command(name=name, description=description)
    async def dvach(self, ctx: Context):
        try:
            link = await self.dvach_api.get_random_url()
            await ctx.send(link)
        except:
            raise RequestNetworkError

async def setup(bot):
    await bot.add_cog(Dvach(bot))
