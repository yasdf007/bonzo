from discord.ext.commands import Cog
from bot import Bot

class Settings(Cog):
    def __init__(self, bot):
        self.bot: Bot = bot


async def setup(bot):
    await bot.add_cog(Settings(bot))
