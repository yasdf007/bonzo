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

    # функция, удаляющая X сообщений из чата
    @commands.command(name='clear', description='Очищает последние x сообщений (только для разработчиков)')
    async def clear(self, ctx, count: int):

        # создание читаемого списка ролей запрашивающего выполнения команды
        authorroles = [y.name.lower() for y in ctx.author.roles]
        if 'bonzodev' in authorroles:  # проверяем, есть ли в ролях пользователя роль bonzodev
            # удаляем запрошенное кол-во сообщений!
            await discord.TextChannel.purge(ctx.message.channel, limit=count + 1)
            await ctx.send("очистил %s сообщений!" % count)  # отправляем отчёт
            await sleep(2)  # ждём 2 секунды
            # удаляем отчёт
            await discord.TextChannel.purge(ctx.message.channel, limit=1)
        else:
            await ctx.send('{0.author.mention}'.format(ctx) + ' **слыш,** тебе нельзя такое исполнять')


def setup(bot):
    bot.add_cog(Clear(bot))
