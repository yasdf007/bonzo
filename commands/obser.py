from discord.ext.commands import Cog, command
from discord.ext.commands.context import Context
from discord import File
from discord_slash import SlashContext, cog_ext
from config import guilds

name = 'obser'
description = 'Виды обсёров.......'


class obser(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name=name, description=description)
    async def obser_prefix(self, ctx: Context):
        await self.obser(ctx)

    @cog_ext.cog_slash(name=name, description=description)
    async def obser_slash(self, ctx: SlashContext):
        await self.obser(ctx)

    async def obser(self, ctx):
        await ctx.send(content='https://www.youtube.com/watch?v=Nv9x7E5tnoA', file=File('./static/pictOBSER.jpg'))


def setup(bot):
    bot.add_cog(obser(bot))
