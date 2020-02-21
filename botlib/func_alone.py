# created by ムAloneStranger (c) 2020. 
# вносить дальнейшие изменения в этот файл следует только автору файла.

# необходимое каждому модулю команд начало
from bonzoinit import bot
from random import randint

@bot.command()
async def randomcat(ctx):
    await ctx.send('https://cataas.com/cat?' + str(randint(0, 10**6)))
