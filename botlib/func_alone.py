# created by ムAloneStranger (c) 2020. 

# необходимое каждому модулю команд начало
from bonzoboot import bot

# импорт дополнительных модулей (индивидуальных)
import discord
from random import randint
from asyncio import sleep

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
    embed.set_thumbnail(url=server.icon_url)
    embed.add_field(name='**Название:**', value=str(server.name), inline=False)
    embed.add_field(name='**Количество участников:**', value=str(server.member_count), inline=False)
    embed.set_footer(text='/by bonzo/ for @' + ctx.message.author.name)
    await ctx.send(embed=embed)

# функция, удаляющая X сообщений из чата
@bot.command()
async def clear(ctx, count: int):
    authorroles = [y.name.lower() for y in ctx.author.roles] # создание читаемого списка ролей запрашивающего выполнения команды
    if 'bonzodev' in authorroles:
        await discord.TextChannel.purge(ctx.message.channel, limit=count + 1)
        await ctx.send("очистил %s сообщений!" % count)
        await sleep(2)
        await discord.TextChannel.purge(ctx.message.channel, limit=1)
    else:
        await ctx.send('{0.author.mention}'.format(ctx)+ ' **слыш,** тебе нельзя такое исполнять')

# eval - запуск кода от лица бота овнером через discord.
@bot.command() 
async def evala(ctx, evcode=None):
    ownerids = [221246477630963722, 196314341572608000, 393807398047055883]
    if evcode == None:
        await ctx.send("укажите код для экзекьюции.")
    else:
        if ctx.author.id in ownerids:
            execute = eval(str(evcode))
            await execute
        else: 
            await ctx.send("ты безправное чмо " + '{0.author.mention}'.format(ctx))
