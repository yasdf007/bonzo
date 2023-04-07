from commands.resources.AutomatedMessages import automata
from discord.ext.commands import Cog, is_owner, hybrid_command, Context
from discord.ext.commands.errors import CommandInvokeError, NotOwner
from bot import Bot

name = "evala"
description = "Исполняет код (только для разработчиков)"


class evala(Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    # Обработка ошибок

    async def cog_command_error(self, ctx: Context, error):
        if isinstance(error, CommandInvokeError):
            await ctx.send(
                embed=automata.generateEmbErr("Ошибка при выполении запроса")
            )

        if isinstance(error, NotOwner):
            pass

    # eval - запуск кода от лица бота овнером через discord.
    # не следует использовать рядовым пользователям. дословно закомментировано не будет (!)
    @hybrid_command(name=name, description=description)
    @is_owner()
    async def evala(self, ctx: Context, evcode: str):
        if not evcode:
            raise CommandInvokeError()

        execute = eval(evcode)

        await ctx.message.delete()

        await execute


async def setup(bot):
    await bot.add_cog(evala(bot))
