from discord import TextChannel
from discord.ext.commands import Cog, CommandInvokeError, command
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
    @command(name=name, description=description)
    async def evala(self, ctx, evcode):
        ownerids = [221246477630963722, 196314341572608000,
                    393807398047055883]  # определяем овнеров
        if evcode:
            if ctx.author.id in ownerids:  # проверяем, овнер ли запросил команду?
                execute = eval(str(evcode))
                # удаляем команду
                await TextChannel.purge(ctx.message.channel, limit=1)
                await execute
            else:
                await ctx.send("ты бесправное чмо " + '{0.author.mention}'.format(ctx))
        else:
            # Ошибка
            raise CommandInvokeError()


def setup(bot):
    bot.add_cog(evala(bot))
