from discord.ext import commands
from random import randint


class randomCat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Обработа ошибок
    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send('Нужно ввести количество ссылок (до 2)')

    @commands.command(name='randomcat', description='Отправляет случайного котика :3')
    async def randomcat(self, ctx, Num=None):
        # Если количество не указано
        if Num is None:
            # Отправляем одну ссылку
            cat = await self.makeCatUrl()
            await ctx.send(cat)

        # Если указано
        else:
            Num = int(Num)

            if Num > 2:
                # Если число больше максимума, отправляем ошибку
                raise commands.CommandInvokeError()

            else:
                # Делаем Num ссылок
                for _ in range(0, Num):
                    cat = await self.makeCatUrl()
                    await ctx.send(cat)
    # Функци создания картинки

    async def makeCatUrl(self):
        return 'https://cataas.com/cat?' + str(randint(0, 10**6))


def setup(bot):
    bot.add_cog(randomCat(bot))
