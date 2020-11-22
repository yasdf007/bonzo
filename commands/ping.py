from discord.ext import commands


class ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Задержка
    @commands.command(name='ping', description='Понг!')
    async def ping(self, ctx):
        botLatency = round(self.bot.latency * 1000, 2)
        await ctx.send('Pong! ' + str(botLatency) + 'ms ' + '(задержка)')


def setup(bot):
    bot.add_cog(ping(bot))
