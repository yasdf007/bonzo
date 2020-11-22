from discord.ext import commands
from discord import File

name='obser'
description='Виды обсёров.......'

class obser(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Прикол ахахха
    @commands.command(name=name, description=description)
    async def obser(self, ctx):
        await ctx.send(content='https://www.youtube.com/watch?v=Nv9x7E5tnoA', file=File('./static/pictOBSER.jpg'))


def setup(bot):
    bot.add_cog(obser(bot))
