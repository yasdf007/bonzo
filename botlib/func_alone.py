# created by ムAloneStranger (c) 2020. 

# необходимое каждому модулю команд начало
from bonzoboot import bot

# импорт дополнительных модулей (индивидуальных)
import discord
from random import randint
from asyncio import sleep

# функция, отправляющая рандомного котика :3
@bot.command()
async def randomcat(ctx, Num=None):
    if Num is None:
        await ctx.send('https://cataas.com/cat?' + str(randint(0, 10**6)))
    else:
        Num = int(Num)
        if Num > 2:
            await ctx.send("Превышено максимальное количество ссылок")
        else:
            for i in range(0, Num):
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
    if 'bonzodev' in authorroles: # проверяем, есть ли в ролях пользователя роль bonzodev
        await discord.TextChannel.purge(ctx.message.channel, limit=count + 1) # удаляем запрошенное кол-во сообщений!
        await ctx.send("очистил %s сообщений!" % count) # отправляем отчёт
        await sleep(2) # ждём 2 секунды
        await discord.TextChannel.purge(ctx.message.channel, limit=1) # удаляем отчёт
    else:
        await ctx.send('{0.author.mention}'.format(ctx)+ ' **слыш,** тебе нельзя такое исполнять')

# функция, отправляющая инвайт-ссылку бота в чат
@bot.command()
async def invite(ctx):
    embedd = discord.Embed(title='**зовём /bonzo/ на ваш сервер...**', colour=0xb84000)
    embedd.set_thumbnail(url='https://cdn.discordapp.com/avatars/680132907859443790/3d059b62a6c5b6dd6fa46fdfd432f009.webp?size=256')
    embedd.add_field(name='кликните вот', value='[сюда](https://discordapp.com/api/oauth2/authorize?client_id=680132907859443790&permissions=8&scope=bot)')
    embedd.set_footer(text="/by bonzo/ for @" + ctx.message.author.name)
    await ctx.send(embed=embedd)

