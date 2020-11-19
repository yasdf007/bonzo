from discord import Embed
from discord.ext import commands
from asyncio import sleep
from random import randint


class testingEdit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def testEdit(self, ctx):
        embed = Embed(
            title='Тестирую', color=0x543964)

        toEdit = await ctx.send(embed=embed)

        for _ in range(4):
            color = randint(0, 0xFFFFFF)
            embed.colour = color
            await toEdit.edit(embed=embed)
            await sleep(0.25)


def setup(bot):
    bot.add_cog(testingEdit(bot))
