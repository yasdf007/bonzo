from discord import TextChannel
from discord.ext.commands import Cog, CommandInvokeError, command, has_role
name = 'evala'
description = 'Исполняет код (только для разработчиков)'


class evala(Cog):
    def __init__(self, bot):
        self.bot = bot
    # Обработка ошибок

    async def cog_command_error(self, ctx, error):
        if isinstance(error, CommandInvokeError):
            await ctx.send('Ошибка при выполении запроса')

    # eval - запуск кода от лица бота овнером через discord.
    # не следует использовать рядовым пользователям. дословно закомментировано не будет (!)
    @has_role('bonzodev')
    @command(name=name, description=description)
    async def evala(self, ctx, evcode: str):
        if evcode:
            execute = eval(evcode)
            # удаляем команду
            await ctx.message.delete()

            await execute
        else:
            # Ошибка
            raise CommandInvokeError()


def setup(bot):
    bot.add_cog(evala(bot))
