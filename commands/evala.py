from discord.ext.commands import Cog, is_owner, hybrid_command, Context
from discord.ext.commands.errors import CommandInvokeError
from discord.app_commands import guilds
from bot import Bot
from config import MAIN_GUILD

name = "evala"
description = "Исполняет код (только для разработчиков)"


class evala(Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    # eval - запуск кода от лица бота овнером через discord.
    # не следует использовать рядовым пользователям. дословно закомментировано не будет (!)
    @hybrid_command(name=name, description=description)
    @guilds(MAIN_GUILD)
    @is_owner()
    async def evala(self, ctx: Context, evcode: str):
        if not evcode:
            raise CommandInvokeError()

        execute = eval(evcode)

        await ctx.message.delete()

        await execute


async def setup(bot):
    await bot.add_cog(evala(bot))
