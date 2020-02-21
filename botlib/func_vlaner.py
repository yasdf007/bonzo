# created by vlaner (c) 2020.
# вносить дальнейшие изменения в этот файл следует только автору файла.

# необходимое каждому модулю команд начало
from discord.ext import commands
from bonzoinit import bot

# функция говорит сама за себя
@bot.command()
async def da(ctx): 
    await ctx.send('{0.author.mention}'.format(ctx) + ' ' + "ПИЗДА АХАХАХХАХАХАХАХААХАХААХА")
