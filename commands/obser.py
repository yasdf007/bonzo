from discord.ext import commands


class obser(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def obser(self, ctx):
        await ctx.send("https://sun1-16.userapi.com/NjDsxJrEr31xWKtAVMQiKZ5CzDH6cGS9XhaB-g/ZBfUwNHhdzw.jpg")


def setup(bot):
    bot.add_cog(obser(bot))
