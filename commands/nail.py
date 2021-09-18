from discord.ext.commands import Cog, command
from discord import File
from discord_slash import SlashContext, cog_ext
from config import guilds

name = 'nail'
description = 'Бегающий гвоздь'


class Nail(Cog):
    def __init__(self, bot):
        self.bot = bot

    # Прикол ахахха
    @cog_ext.cog_slash(name=name, description=description, guild_ids=guilds)
    async def nail(self, ctx: SlashContext):
        await ctx.send(file=File('./static/nail.jpg'))


def setup(bot):
    bot.add_cog(Nail(bot))
