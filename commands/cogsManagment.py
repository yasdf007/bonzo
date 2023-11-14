from discord.ext.commands import Cog
from discord import app_commands, Interaction
import traceback
from bot import Bot
from config import MAIN_GUILD, DEBUG_GUILD
from discord.app_commands import guilds
from .resources.checks import check_is_owner
import discord

class CogsManagement(Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @app_commands.command(name="load", description="Загружает ког")
    @guilds(MAIN_GUILD)
    @check_is_owner()
    async def load_cog(self, inter: Interaction, cog: str):
        try:
            await self.bot.load_extension("commands." + cog)
        except Exception as e:
            return await inter.response.send_message(f"Невозможно загрузить ког: {traceback.format_exc()}")
        await inter.response.send_message(f"Ког {cog} загружен")

    @app_commands.command(name="unload", description="Выгружает ког")
    @guilds(MAIN_GUILD)
    @check_is_owner()
    async def unload_cog(self, inter: Interaction, cog: str):
        try:
            await self.bot.unload_extension("commands." + cog)
        except Exception as e:
            return await inter.response.send_message(f"Невозможно выгрузить ког: {traceback.format_exc()}")

        await inter.response.send_message(f"Ког {cog} выгружен")

    @app_commands.command(name="reload", description="Перезагружает ког")
    @guilds(MAIN_GUILD)
    @check_is_owner()
    async def reload_reload(self, inter: Interaction, cog: str):
        try:
            await self.bot.unload_extension("commands." + cog)
            await self.bot.load_extension("commands." + cog)
        except Exception as e:
            return await inter.response.send_message(f"Невозможно перезагрузить ког {traceback.format_exc()}")

        await inter.response.send_message(f"Ког {cog} перезагружен")


    @app_commands.command(name="sync", description="Синхронизирует команды")
    @guilds(MAIN_GUILD)
    @check_is_owner()
    async def sync_cmds(self, inter: Interaction, guild_id: str=None):
        if guild_id:
            guild = discord.Object(int(guild_id))
            synced = await self.bot.tree.sync(guild=guild)
        else:
            synced = await self.bot.tree.sync()
        print(synced)
        await inter.response.send_message('Команды синхронизированы')

async def setup(bot):
    await bot.add_cog(CogsManagement(bot))
