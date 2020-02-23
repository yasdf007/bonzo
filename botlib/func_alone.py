# created by ムAloneStranger (c) 2020. 

# необходимое каждому модулю команд начало
from bonzoboot import bot
from random import randint
import discord

# функция, отправляющая рандомного котика :3
@bot.command()
async def randomcat(ctx):
    await ctx.send('https://cataas.com/cat?' + str(randint(0, 10**6)))

# функция, отправляющая информацию о сервере
@bot.command()
async def serverinfo(ctx):
    server = ctx.message.guild
    embed = discord.Embed(
        title = '**Информация о сервере:**',
        colour = 0x7D07DE
    )
#   embed.set_footer(text='', icon_url=server.icon_url) # не даёт необходимый результат
    embed.add_field(name='Название:', value=str(server.name), inline=False)
    embed.add_field(name='Количество участников:', value=str(server.member_count), inline=False)
    await ctx.send(embed=embed)
