# created by nohame (c) 2020.
# вносить дальнейшие изменения в этот файл следует только автору файла.

# необходимое каждому модулю команд начало
from bonzoboot import bot

@bot.command 
async def jf(ctx): 
   embed=discord.Embed(
title="Команды бота ахахахахахахаха",
colour=0xffff00) 
#головная часть. Последняя штука для цвета полоски
embed.add_field(name="b/da", value="ладно", inline=False) 
#первый шрифт жирный, второй тонкий внизу 
embed.add_field(name="b/randomcat", value="котик", inline=False) 
#смещение влево (False) 
embed.add_field(name="b/ping", inline=False)
embed.set_author('{0.author.mention}'.format(ctx)) 
#упоминание отправителей 
embed.set_footer(text="вставить текст")  
#маленькая подпись в самом низу
await send.ctx(embed=embed) 
#сброс бомбы на пiндосов 
