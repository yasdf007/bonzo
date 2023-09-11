from discord import app_commands, Interaction
from discord.ext.commands import Cog
from bot import Bot

name = "ping"
description = "Понг!"


class ping(Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    # Задержка
    @app_commands.command(name=name, description=description)
    async def ping(self, inter: Interaction):
        botLatency = round(inter.client.latency * 1000, 2)
        await inter.response.send_message(f"Pong! {str(botLatency)}ms (задержка)")


async def setup(bot):
    await bot.add_cog(ping(bot))
