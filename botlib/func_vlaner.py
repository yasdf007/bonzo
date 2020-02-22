# created by vlaner (c) 2020.
# вносить дальнейшие изменения в этот файл следует только автору файла.

# необходимое каждому модулю команд начало
from bonzoboot import bot
from random import randint
from random import sample

# функция говорит сама за себя
@bot.command()
async def da(ctx): 
    await ctx.send('{0.author.mention}'.format(ctx) + ' ' + "ПИЗДА АХАХАХХАХАХАХАХААХАХААХА")

#dota 2 roll
@bot.command()
async def roll(ctx, a=None, b=None):
    if a is None and b is None:
        await ctx.send('{0.author.mention}'.format(ctx) + ' Random Number is: ' + str(randint(1, 100)))
    else:
        a = int(a)
        b = int(b)
        await ctx.send('{0.author.mention}'.format(ctx) + ' Random Number is: ' + str(randint(a, b)))

@bot.command()
async def pict(ctx):
    symbols = 'abcdefghijklmnopqrstuvwxyz1234567890'
    url = 'https://prnt.sc/'
    symbolsStr = ''.join(sample(symbols, 6)) # делаем случайную строку из 6 символов
    url += symbolsStr # соединяем строку выше с ссылкой url
    await ctx.send(url)

