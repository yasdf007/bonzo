from discord.ext.commands import Cog
from discord.ext.commands.errors import CommandInvokeError
from discord.app_commands import guilds
from bot import Bot
from config import MAIN_GUILD
from discord import Interaction, app_commands
from .resources.checks import check_is_owner

class evala(Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    # eval - запуск кода от лица бота овнером через discord.
    # не следует использовать рядовым пользователям. дословно закомментировано не будет (!)
    @app_commands.command(name="evala", description="Исполняет код (только для разработчиков)")
    @app_commands.guilds(MAIN_GUILD)
    @check_is_owner()
    async def evala(self, inter: Interaction, evcode: str):
        if not evcode:
            raise CommandInvokeError()

        eval(evcode)

async def setup(bot):
    if False:
        await bot.add_cog(evala(bot))
