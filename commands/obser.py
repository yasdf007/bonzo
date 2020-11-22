from discord.ext import commands
from discord import File


class obser(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='obser', description='Виды обсёров.......')
    async def obser(self, ctx):
        await ctx.send(file=File('./static/pictOBSER.jpg'))


def setup(bot):
    bot.add_cog(obser(bot))
