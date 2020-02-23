# created by nohame (c) 2020.

# необходимое каждому модулю команд начало
from bonzoboot import bot
import discord

@bot.command()
async def help(ctx):
   embed=discord.Embed(
   title='**Команды бота:**', # title - головная часть, colour - hex-код цвета полоски
   colour=0xffff00)
#  embed.set_thumbnail(url=str(discord.AppInfo.icon)) # не работает.
   embed.add_field(name='da', value='Отправит в ответ ПИЗДУ)', inline=False) # inline отвечает за смещение вправо (репрезентация в одной строке)
   embed.add_field(name='ping', value='Понг!', inline=False)
   embed.add_field(name='roll', value='Ролит как в доте или между двумя числами', inline=False)
   embed.add_field(name='randomcat', value='Отправляет случайного котика :3', inline=False)
   embed.add_field(name='pict', value='Отправляет случайное изображение из prnt.sc :o', inline=False) 
   embed.add_field(name='serverinfo', value='Показывает информацию о сервере', inline=False)
#  embed.add_field(name='', value='', inline=)
   embed.set_footer(text="-------") # подпись внизу
   await ctx.send(embed=embed)
