from discord.ext.commands import Cog, command
from discord.ext.commands.context import Context
from discord import File
from discord_slash import SlashContext, cog_ext
from config import guilds

name = 'nail'
description = 'Бегающий гвоздь'


class Nail(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name=name, description=description)
    async def nail_prefix(self, ctx: Context):
        await self.nail(ctx)

    @cog_ext.cog_slash(name=name, description=description)
    async def nail_slash(self, ctx: SlashContext):
        await self.nail(ctx)
    # Прикол ахахха

    async def nail(self, ctx):
        await ctx.send(file=File('./static/nail.jpg'))


def setup(bot):
    bot.add_cog(Nail(bot))
