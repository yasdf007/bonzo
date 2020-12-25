from discord.ext.commands import Cog, CommandInvokeError, command
from random import randint

name = 'randomcat'
description = 'Отправляет случайного котика :3'


class randomCat(Cog):
    def __init__(self, bot):
        self.bot = bot

    # Обработа ошибок
    async def cog_command_error(self, ctx, error):
        if isinstance(error, CommandInvokeError):
            await ctx.send('Нужно ввести количество ссылок (до 2)')

    @command(name=name, description=description)
    async def randomcat(self, ctx, num=None):
        # Если количество не указано
        if num is None:
            # Отправляем одну ссылку
            cat = await self.makeCatUrl()
            await ctx.send(cat)

        # Если указано
        else:
            num = int(num)

            if num > 2:
                # Если число больше максимума, отправляем ошибку
                raise CommandInvokeError()

            else:
                # Делаем Num ссылок
                for _ in range(0, num):
                    cat = await self.makeCatUrl()
                    await ctx.send(cat)
    # Функци создания картинки

    async def makeCatUrl(self):
        return 'https://cataas.com/cat?' + str(randint(0, 10**6))


def setup(bot):
    bot.add_cog(randomCat(bot))
