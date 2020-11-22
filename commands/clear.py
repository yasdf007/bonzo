import discord
from discord.ext import commands
from asyncio import sleep


class Clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Обработка ошибок
    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('Нужно ввести количество сообщений целым числом')

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Нужно ввести количество сообщений целым числом')

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.send('**слыш,** тебе нельзя такое исполнять')

    # функция, удаляющая X сообщений из чата
    @commands.has_role('bonzodev')
    @commands.command(name='clear', description='Очищает последние x сообщений (только для разработчиков)')
    async def clear(self, ctx, count: int):
        # удаляем запрошенное кол-во сообщений!
        await discord.TextChannel.purge(ctx.message.channel, limit=count + 1)
        await ctx.send("очистил %s сообщений!" % count)  # отправляем отчёт
        await sleep(2)  # ждём 2 секунды
        # удаляем отчёт
        await discord.TextChannel.purge(ctx.message.channel, limit=1)


def setup(bot):
    bot.add_cog(Clear(bot))
