from discord.ext import commands
from random import sample

name='pict'
description='Отправляет случайное изображение из prnt.sc :o'

class pict(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Обработка ошибок
    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send('Нужно ввести количество ссылок (до 2)')

    @commands.command(name=name, description=description)
    async def pict(self, ctx, Num=None):
        # Если количество не указано
        if Num is None:
            # Делаем одну ссылку
            url = await self.makePictUrl()
            await ctx.send(url)
        # Если количество указано
        else:
            Num = int(Num)

            if Num > 2:
                # Если число больше максимума, отправляем ошибку
                raise commands.CommandInvokeError()
            # Делаем Num ссылок
            for _ in range(0, Num):
                url = await self.makePictUrl()
                await ctx.send(url)

    # Функция, генерирующая ссылку
    async def makePictUrl(self):
        symbols = 'abcdefghijklmnopqrstuvwxyz1234567890'
        url = 'https://prnt.sc/'
        # делаем случайную строку из 6 символов
        symbolsStr = ''.join(sample(symbols, 6))
        url += symbolsStr  # соединяем строку выше с ссылкой url
        return url


def setup(bot):
    bot.add_cog(pict(bot))
