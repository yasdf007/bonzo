from discord.ext.commands import Cog, command, CommandInvokeError
from random import choices
from typing import Optional
from string import ascii_lowercase, digits
name = 'pict'
description = 'Отправляет случайное изображение из prnt.sc :o'


class pict(Cog):
    url = 'https://prnt.sc/'

    def __init__(self, bot):
        self.bot = bot

    # Обработка ошибок

    async def cog_command_error(self, ctx, error):
        if isinstance(error, CommandInvokeError):
            await ctx.message.reply('Нужно ввести количество ссылок (до 2)')

    @command(name=name, description=description)
    async def pict(self, ctx, num: Optional[int]):
        # Если количество не указано
        if num is None:
            # Делаем одну ссылку
            url = await self.makePictUrl()
            await ctx.message.reply(url)

        # Если количество указано
        elif num > 2:
            # Если число больше максимума, отправляем ошибку
            raise CommandInvokeError()

        else:
            # Делаем num ссылок
            for _ in range(0, num):
                url = await self.makePictUrl()
                await ctx.message.reply(url)

    # Функция, генерирующая ссылку
    async def makePictUrl(self):
        # делаем случайную строку из 6 символов
        symbolsStr = ''.join(choices(ascii_lowercase + digits, k=6))
        # соединяем строку с ссылкой url
        result = self.url + symbolsStr
        return result


def setup(bot):
    bot.add_cog(pict(bot))
