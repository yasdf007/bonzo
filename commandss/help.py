import discord
from discord.ext import commands


class helpNew(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help2(self, ctx):
        await ctx.send(discord.ext.commands.HelpCommand())


def setup(bot):
    bot.add_cog(helpNew(bot))
