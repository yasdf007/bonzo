from discord.ext.commands import Cog, hybrid_command, Context
from bot import Bot

name = "ping"
description = "Понг!"


class ping(Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    # Задержка
    @hybrid_command(name=name, description=description)
    async def ping(self, ctx: Context):
        botLatency = round(ctx.bot.latency * 1000, 2)
        await ctx.send(f"Pong! {str(botLatency)}ms (задержка)")


async def setup(bot):
    await bot.add_cog(ping(bot))
