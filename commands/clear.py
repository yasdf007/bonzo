from commands.resources.AutomatedMessages import automata
from discord import TextChannel
from discord.ext.commands import Cog, has_permissions, command, bot_has_permissions
from asyncio import sleep
from discord.ext.commands.errors import BadArgument, MissingRequiredArgument, MissingPermissions, CommandInvokeError, BotMissingPermissions
name = 'clear'
description = 'Очищает последние x сообщений (для персонала сервера)'


class Clear(Cog):
    def __init__(self, bot):
        self.bot = bot

    # Обработка ошибок
    async def cog_command_error(self, ctx, error):
        if isinstance(error, (MissingRequiredArgument, BadArgument)):
            await ctx.send(embed=automata.generateEmbErr('Введите количество сообщений целым числом'))

        if isinstance(error, MissingPermissions):
            await ctx.send(embed=automata.generateEmbErr('У вас недостаточно прав для исполнения данной команды'))

        if isinstance(error, CommandInvokeError):
            await ctx.send(embed=automata.generateEmbErr('Ошибка при исполнении команды'))

        if isinstance(error, BotMissingPermissions):
            await ctx.send(embed=automata.generateEmbErr('У bonzo недостаточно прав для исполнения данной команды (Manage Messages)'))

    # функция, удаляющая X сообщений из чата
    @has_permissions(manage_messages=True)
    @bot_has_permissions(manage_messages=True)
    @command(name=name, description=description)
    async def clear(self, ctx, count: int):
        # удаляем запрошенное кол-во сообщений!
        await TextChannel.purge(ctx.message.channel, limit=count + 1, bulk=True)
        # отправляем отчёт
        msg = await ctx.send(f'Очистил {count} сообщений!')
        await sleep(2)  # ждём 2 секунды
        # удаляем отчёт
        await msg.delete()


def setup(bot):
    bot.add_cog(Clear(bot))
