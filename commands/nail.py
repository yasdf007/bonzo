from discord.ext import commands
from discord import File

name = 'nail'
description = 'Бегающий гвоздь'


class Nail(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Прикол ахахха
    @commands.command(name=name, description=description)
    async def nail(self, ctx):
        await ctx.send(file=File('./static/nail.jpg'))


def setup(bot):
    bot.add_cog(Nail(bot))
