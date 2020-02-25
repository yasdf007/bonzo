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

@bot.command()
async def clear(ctx, count: int):
    abc = [y.name.lower() for y in ctx.author.roles]
    if 'bonzodev' in abc:
        await discord.TextChannel.purge(ctx.message.channel, limit=count + 1)
        await ctx.send("очистил %s сообщений!" % count)
        await sleep(2)
        await discord.TextChannel.purge(ctx.message.channel, limit=1)
    else:
        await ctx.send('{0.author.mention}'.format(ctx)+ ' **слыш,** тебе нельзя такое исполнять')
