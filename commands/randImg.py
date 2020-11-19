from discord.ext import commands
from random import sample
import requests
from PIL import Image
from io import BytesIO


class randImg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(error)

    @commands.cooldown(rate=1, per=5)
    @commands.command(pass_context=True)
    async def randImg(self, ctx):
        url = 'https://i.imgur.com/'
        symbols = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

        randSymbols = ''.join(sample(symbols, 5))
        iImgurUrl = url + randSymbols + '.png'
        req = requests.get(iImgurUrl, headers={'User-Agent': 'Mozilla/5.0'})

        img = Image.open(BytesIO(req.content))
        if img.size[0] == 161 and img.size[1] == 81:
            await ctx.invoke(await self.randImg(ctx))
        else:
            await ctx.send(iImgurUrl)


def setup(bot):
    bot.add_cog(randImg(bot))
