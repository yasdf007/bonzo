from discord.ext.commands import Cog, command
from discord.ext.commands.context import Context
from config import guilds
from discord_slash import SlashContext, cog_ext

name = "ping"
description = "Понг!"


class ping(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name=name, description=description)
    async def ping_prefix(self, ctx: Context):
        await self.ping(ctx)

    @cog_ext.cog_slash(name=name, description=description)
    async def ping_slash(self, ctx: SlashContext):
        await self.ping(ctx)

    # Задержка

    async def ping(self, ctx):
        botLatency = round(ctx.bot.latency * 1000, 2)
        await ctx.send(f"Pong! {str(botLatency)}ms (задержка)")


def setup(bot):
    bot.add_cog(ping(bot))
