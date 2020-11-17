from discord.ext import commands
from random import randint
from random import sample
import requests
from PIL import Image
from io import BytesIO

class vlanerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def obser(self, ctx):
        await ctx.send("https://sun1-16.userapi.com/NjDsxJrEr31xWKtAVMQiKZ5CzDH6cGS9XhaB-g/ZBfUwNHhdzw.jpg")

    #dota 2 roll
    @commands.command()
    async def roll(self, ctx, a=None, b=None):
        if a is None and b is None:
            await ctx.send('{0.author.mention}'.format(ctx) + ' Random Number is: ' + str(randint(1, 100)))
        elif b is None:
            a = int(a)
            if a <= 10**6:
                await ctx.send('{0.author.mention}'.format(ctx) + ' Random Number is: ' + str(randint(1, a)))
            else: 
                await ctx.send('{0.author.mention}'.format(ctx) + ' больше мильёна роллить не буду')
        else:
            a, b = int(a), int(b)
            if b <= 10**6:
                await ctx.send('{0.author.mention}'.format(ctx) + ' Random Number is: ' + str(randint(a, b)))
            else:
                await ctx.send('{0.author.mention}'.format(ctx) + ' больше мильёна роллить не буду')

    @commands.command()
    async def pict(self, ctx, Num=None):
        if Num is None:
            symbols = 'abcdefghijklmnopqrstuvwxyz1234567890'
            url = 'https://prnt.sc/'
            symbolsStr = ''.join(sample(symbols, 6)) # делаем случайную строку из 6 символов
            url += symbolsStr # соединяем строку выше с ссылкой url
            await ctx.send(url)
        else:
            Num = int(Num)
            if Num > 2:
                await ctx.send("Превышено допустимое количество ссылок")
            else:
                for i in range(0, Num):
                    symbols = 'abcdefghijklmnopqrstuvwxyz1234567890'
                    url = 'https://prnt.sc/'
                    symbolsStr = ''.join(sample(symbols, 6)) # делаем случайную строку из 6 символов
                    url += symbolsStr # соединяем строку выше с ссылкой url
                    await ctx.send(url)

    @commands.command(pass_context=True)
    async def randImg(self, ctx):
        url = 'https://i.imgur.com/'
        symbols = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

        randSymbols = ''.join(sample(symbols, 5))
        iImgurUrl = url + randSymbols + '.png'
        req = requests.get(iImgurUrl, headers={'User-Agent': 'Mozilla/5.0'})

        img = Image.open(BytesIO(req.content))
        if img.size[0] == 161 and img.size[1] == 81:
            await randImg(ctx)
        else:
            await ctx.send(iImgurUrl)

    @commands.command()
    async def ping(self, ctx):
        await ctx.send('Pong! ' + str(round(self.bot.latency, 3)) + 'ms ' + '(задержка)')

def setup(bot):
    bot.add_cog(vlanerCog(bot))