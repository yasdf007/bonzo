from discord.ext import commands
from random import sample


class pict(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send('Нужно ввести количество ссылок (до 2)')

    @commands.command(name='pict', description='Отправляет случайное изображение из prnt.sc :o')
    async def pict(self, ctx, Num=None):
        if Num is None:
            url = await self.makePictUrl()
            await ctx.send(url)
        else:
            Num = int(Num)

            if Num > 2:
                raise commands.CommandInvokeError()

            for _ in range(0, Num):
                url = await self.makePictUrl()
                await ctx.send(url)

    async def makePictUrl(self):
        symbols = 'abcdefghijklmnopqrstuvwxyz1234567890'
        url = 'https://prnt.sc/'
        # делаем случайную строку из 6 символов
        symbolsStr = ''.join(sample(symbols, 6))
        url += symbolsStr  # соединяем строку выше с ссылкой url
        return url


def setup(bot):
    bot.add_cog(pict(bot))
