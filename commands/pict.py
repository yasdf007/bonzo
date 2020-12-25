from discord.ext.commands import Cog, command, CommandInvokeError
from random import sample

name = 'pict'
description = 'Отправляет случайное изображение из prnt.sc :o'


class pict(Cog):
    def __init__(self, bot):
        self.bot = bot

    # Обработка ошибок
    async def cog_command_error(self, ctx, error):
        if isinstance(error, CommandInvokeError):
            await ctx.send('Нужно ввести количество ссылок (до 2)')

    @command(name=name, description=description)
    async def pict(self, ctx, num=None):
        # Если количество не указано
        if num is None:
            # Делаем одну ссылку
            url = await self.makePictUrl()
            await ctx.send(url)
        # Если количество указано
        else:
            num = int(num)

            if num > 2:
                # Если число больше максимума, отправляем ошибку
                raise CommandInvokeError()
            # Делаем num ссылок
            for _ in range(0, num):
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
