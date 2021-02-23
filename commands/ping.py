from discord.ext.commands import Cog, command

name = 'ping'
description = 'Понг!'


class ping(Cog):
    def __init__(self, bot):
        self.bot = bot

    # Задержка
    @command(name=name, description=description)
    async def ping(self, ctx):
        botLatency = round(self.bot.latency * 1000, 2)
        await ctx.message.reply('Pong! ' + str(botLatency) + 'ms ' + '(задержка)')


def setup(bot):
    bot.add_cog(ping(bot))
