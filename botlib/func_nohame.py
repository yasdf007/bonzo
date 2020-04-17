# created by nohame (c) 2020.

# необходимое каждому модулю команд начало
from bonzoboot import bot

# импорт дополнительных модулей (индивидуальных)
import discord

@bot.command()
async def help(ctx):
   embed=discord.Embed(
   title='**Команды бота:**', # title - головная часть, colour - hex-код цвета полоски
   colour=0xffff00)
   embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/680132907859443790/3d059b62a6c5b6dd6fa46fdfd432f009.webp?size=256')
   embed.add_field(name='da', value='Отправит в ответ ПИЗДУ)', inline=False) # inline отвечает за смещение вправо (репрезентация в одной строке)
   embed.add_field(name='ping', value='Понг!', inline=False)
   embed.add_field(name='roll', value='Ролит как в доте или между двумя числами', inline=False)
   embed.add_field(name='randomcat', value='Отправляет случайного котика :3', inline=False)
   embed.add_field(name='pict', value='Отправляет случайное изображение из prnt.sc :o', inline=False) 
   embed.add_field(name='randImg', value='Отправляет случайное изображение из imgur', inline=False)
   embed.add_field(name='serverinfo', value='Показывает информацию о сервере', inline=False)
   embed.add_field(name='clear', value='Очищает последние x сообщений (только для разработчиков)', inline=False)
   embed.add_field(name='evala', value='Исполняет код. (только для создателей бота)', inline=False)
   embed.add_field(name='join', value='Присоединяется к войсу! Будет молчать как влаdick после месячных!', inline=True)
   embed.add_field(name='leave', value='Покидает войс! Как влаdick после катки в доту!', inline=True)
#  embed.add_field(name='', value='', inline=)
   embed.set_footer(text="/by bonzo/ for @" + ctx.message.author.name) # подпись внизу
   await ctx.send(embed=embed)

# команда присоединения к vc
# @bot.command() 
# async def joinvc(ctx):
#    if ctx.author.voice and ctx.author.voice.channel:
#       channel = ctx.author.voice.channel
#       await channel.connect() #следовать за вождь
#    else:
#       await ctx.send("{0.author.mention}".format(ctx) + " ты че долбоёб зайди в войс")

# команда отсоединения от vc
# @bot.command() 
# async def leavevc(ctx):
#    voice_client = ctx.bot.voice_clients
#    if voice_client:
#       await ctx.voice_client.disconnect()
#    else:
#       await ctx.send('даун, %s, я не в войсе' %"{0.author.mention}".format(ctx))

