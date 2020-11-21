from discord.ext import commands
from discord import File
from PIL import Image
from io import BytesIO
import requests


class Shakalizator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send('Где фотка')

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(error)

    @commands.cooldown(rate=1, per=5)
    @commands.command(aliases=['шакал', 'сжать', 'shakal'])
    async def shakalizator(self, ctx, imageUrl=None):
        if imageUrl != None:
            requestImage = requests.get(imageUrl)
        else:
            urlFromPhoto = ctx.message.attachments[0].url
            requestImage = requests.get(urlFromPhoto)

        img = Image.open(BytesIO(requestImage.content))
        img = img.resize((450, 450))

        with BytesIO() as image_binary:
            img.save(image_binary, "jpeg", quality=0)
            image_binary.seek(0)
            await ctx.send(file=File(fp=image_binary, filename='now.jpeg'))


def setup(bot):
    bot.add_cog(Shakalizator(bot))
