from discord.ext.commands import Cog
from bonzoboot import guilds
from discord_slash import SlashContext, cog_ext

name = 'ping'
description = 'Понг!'


class ping(Cog):
    def __init__(self, bot):
        self.bot = bot

    # Задержка
    @cog_ext.cog_slash(name=name, description=description, guild_ids=guilds)
    async def ping(self, ctx: SlashContext):
        botLatency = round(ctx.bot.latency * 1000, 2)
        await ctx.send(f'Pong! {str(botLatency)}ms (задержка)')


def setup(bot):
    bot.add_cog(ping(bot))
