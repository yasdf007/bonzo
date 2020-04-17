# created by vlaner (c) 2020.

# необходимое каждому модулю команд начало
from bonzoboot import bot

# импорт дополнительных модулей (индивидуальных)
from random import randint
from random import sample
from bs4 import BeautifulSoup
import requests
from PIL import Image
from io import BytesIO
import youtube_dl
from discord.utils import get
import os
import discord
# функция говорит сама за себя
@bot.command()
async def da(ctx): 
    await ctx.send('{0.author.mention}'.format(ctx) + ' ' + "ПИЗДА АХАХАХХАХАХАХАХААХАХААХА")

#dota 2 roll
@bot.command()
async def roll(ctx, a=None, b=None):
    if a is None and b is None:
        await ctx.send('{0.author.mention}'.format(ctx) + ' Random Number is: ' + str(randint(1, 100)))
    elif b is None:
        a = int(a)
        await ctx.send('{0.author.mention}'.format(ctx) + ' Random Number is: ' + str(randint(1, a)))
    else:
        a, b = int(a), int(b)
        await ctx.send('{0.author.mention}'.format(ctx) + ' Random Number is: ' + str(randint(a, b)))

# отправляет случайный скриншот из базы prnt sc
@bot.command()
async def pict(ctx):
    symbols = 'abcdefghijklmnopqrstuvwxyz1234567890'
    url = 'https://prnt.sc/'
    symbolsStr = ''.join(sample(symbols, 6)) # делаем случайную строку из 6 символов
    url += symbolsStr # соединяем строку выше с ссылкой url
    await ctx.send(url)

# отправляет пинг
@bot.command()
async def ping(ctx):    
    await ctx.send('Pong! ' + str(round(bot.latency, 3)) + 'ms ' + '(задержка)')

# рандом пичка с имгура
@bot.command()
async def randImg(ctx):
    url = 'https://i.imgur.com/'
    symbols = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

    randSymbols = ''.join(sample(symbols, 5))
    iImgurUrl = url + randSymbols + '.png'
    req = requests.get(iImgurUrl, headers={'User-Agent': 'Mozilla/5.0'})

    img = Image.open(BytesIO(req.content))
    if img.size[0] == 161 and img.size[1] == 81:
        await randImg(ctx)
    else:
        await ctx.send(iImgurUrl)

@bot.command()
async def join(ctx):
    channel = ctx.message.author.voice.channel
    voice = get (bot.voice_clients, guild = ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        await channel.connect()

@bot.command()
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get (bot.voice_clients, guild = ctx.guild)
    if voice and voice.is_connected():
        await voice.disconnect()


@bot.command()
async def play(ctx, url: str):
    isSongInDir = os.path.isfile("song.mp3") 
    try:
        if isSongInDir:
            os.remove('song.mp3') # удаление файла, если он есть
            print('EBNYL')
    except PermissionError:
        print('Файла нет') # если нет то погнали
    
    voice = get (bot.voice_clients, guild = ctx.guild)


    ytdl_options = {
        'format' : 'bestaudio/best',
        'postprocessors' : [{
            'key' : 'FFmpegExtractAudio',
            'preferredcodec' : 'mp3',
            'preferredquality' : '192' # битрейт
        }],
    }

    with youtube_dl.YoutubeDL(ytdl_options) as ydl:
        ydl.download([url]) 

    for file in os.listdir('./'):
        if file.endswith('mp3'):
            name = file
            os.rename(file, 'song.mp3')
    voice.play(discord.FFmpegPCMAudio('song.mp3'))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07 # == 100% громкости

    song_name = name.rsplit('-', 2)
    await ctx.send(f'Играет : {song_name[0]}')
    