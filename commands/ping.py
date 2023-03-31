from discord.ext.commands import Cog, hybrid_command
from discord.ext.commands.context import Context

name = "ping"
description = "Понг!"


class ping(Cog):
    def __init__(self, bot):
        self.bot = bot

    # Задержка
    @hybrid_command(name=name, description=description)
    async def ping(self, ctx):
        botLatency = round(ctx.bot.latency * 1000, 2)
        await ctx.send(f"Pong! {str(botLatency)}ms (задержка)")


async def setup(bot):
    await bot.add_cog(ping(bot))
