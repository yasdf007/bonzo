from discord.ext.commands import Cog, command
from bonzoboot import slash, guilds

name = 'ping'
description = 'Понг!'


class ping(Cog):
    def __init__(self, bot):
        self.bot = bot

    # Задержка
    @slash.slash(name=name, description=description, guild_ids=guilds)
    async def ping(self, *ctx):
        botLatency = round(self.bot.latency * 1000, 2)
        await self.send(f'Pong! {str(botLatency)}ms (задержка)')


def setup(bot):
    bot.add_cog(ping(bot))
