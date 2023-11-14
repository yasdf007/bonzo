from discord.ext.commands import Cog
from discord import app_commands, Interaction

from bot import Bot

class Moderation(Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    # функция, удаляющая X сообщений из чата
    @app_commands.command(name="clear", description="Очищает последние x сообщений (для персонала сервера)")
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.bot_has_permissions(manage_messages=True)
    async def clear(self, inter: Interaction, count: int):
        # отправляем отчёт и удаляем его через 5 секунд
        await inter.response.send_message(f"Очистил {count} сообщений!", delete_after=3, ephemeral=True)
        # удаляем запрошенное кол-во сообщений!
        await inter.channel.purge(limit=count, bulk=True)

async def setup(bot):
    await bot.add_cog(Moderation(bot))
