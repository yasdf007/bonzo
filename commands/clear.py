from discord import TextChannel
from discord.ext.commands import Cog, BadArgument, MissingRequiredArgument, MissingRole, CommandInvokeError, has_role, command
from asyncio import sleep
name = 'clear'
description = 'Очищает последние x сообщений (только для разработчиков)'


class Clear(Cog):
    def __init__(self, bot):
        self.bot = bot

    # Обработка ошибок
    async def cog_command_error(self, ctx, error):
        if isinstance(error, BadArgument):
            await ctx.send('Нужно ввести количество сообщений целым числом')

        if isinstance(error, MissingRequiredArgument):
            await ctx.send('Нужно ввести количество сообщений целым числом')

        if isinstance(error, MissingRole):
            await ctx.send('**слыш,** тебе нельзя такое исполнять')

        if isinstance(error, CommandInvokeError):
            await ctx.send('**слыш,** введи число емое')

    # функция, удаляющая X сообщений из чата
    @has_role('bonzodev')
    @command(name=name, description=description)
    async def clear(self, ctx, count: int):
        # удаляем запрошенное кол-во сообщений!
        await TextChannel.purge(ctx.message.channel, limit=count + 1)
        await ctx.send("очистил %s сообщений!" % count)  # отправляем отчёт
        await sleep(2)  # ждём 2 секунды
        # удаляем отчёт
        await TextChannel.purge(ctx.message.channel, limit=1)


def setup(bot):
    bot.add_cog(Clear(bot))
