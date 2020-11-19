from discord.ext import commands
from random import sample


class pict(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def pict(self, ctx, Num=None):
        if Num is None:
            symbols = 'abcdefghijklmnopqrstuvwxyz1234567890'
            url = 'https://prnt.sc/'
            # делаем случайную строку из 6 символов
            symbolsStr = ''.join(sample(symbols, 6))
            url += symbolsStr  # соединяем строку выше с ссылкой url
            await ctx.send(url)
        else:
            Num = int(Num)
            if Num > 2:
                await ctx.send("Превышено допустимое количество ссылок")
            else:
                for i in range(0, Num):
                    symbols = 'abcdefghijklmnopqrstuvwxyz1234567890'
                    url = 'https://prnt.sc/'
                    # делаем случайную строку из 6 символов
                    symbolsStr = ''.join(sample(symbols, 6))
                    url += symbolsStr  # соединяем строку выше с ссылкой url
                    await ctx.send(url)


def setup(bot):
    bot.add_cog(pict(bot))
