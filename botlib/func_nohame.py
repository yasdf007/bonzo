# created by nohame (c) 2020.

# необходимое каждому модулю команд начало
from bonzoboot import bot
import discord

@bot.command()
async def jf(ctx):
   embed=discord.Embed(
   title="Команды бота ахахахахахахаха",
   colour=0xffff00)
   #головная часть. Последняя штука для цвета полоски
   embed.add_field(name="b/da", value="ладно", inline=False) 
   #первый шрифт жирный, второй тонкий внизу 
   embed.add_field(name="b/randomcat", value="котик", inline=False) 
   #смещение влево (False) 
   embed.add_field(name="b/ping", value="пинг!", inline=False)
   #маленькая подпись в самом низу
   embed.set_footer(text="вставить текст")
   #сброс бомбы на пiндосов 
   await ctx.send(embed=embed)
