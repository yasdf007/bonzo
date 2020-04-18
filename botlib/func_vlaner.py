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
@bot.command(pass_context=True)
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
@bot.command(pass_context=True)
async def pict(ctx):
    symbols = 'abcdefghijklmnopqrstuvwxyz1234567890'
    url = 'https://prnt.sc/'
    symbolsStr = ''.join(sample(symbols, 6)) # делаем случайную строку из 6 символов
    url += symbolsStr # соединяем строку выше с ссылкой url
    await ctx.send(url)

# отправляет пинг
@bot.command(pass_context=True)
async def ping(ctx):    
    await ctx.send('Pong! ' + str(round(bot.latency, 3)) + 'ms ' + '(задержка)')

# рандом пичка с имгура
@bot.command(pass_context=True)
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

# команда проигрывания музыки
@bot.command()
async def play(ctx, url: str):
    isSongInDir = os.path.isfile("song.mp3") # есть ли файл song.mp3 в директории бота?
    if isSongInDir: # выполняется, если файл существует
        os.remove('song.mp3') # удаление файла, если он есть
    
    voice = get (bot.voice_clients, guild = ctx.guild) # получает список голосовых соединений бота
    channel = ctx.message.author.voice.channel

    if voice and voice.is_connected():
        await voice.move_to(channel)
        del(voice)
    else:
        await channel.connect()
        del(voice)

    voice = get (bot.voice_clients, guild = ctx.guild) # обновляет список голосовых соединений бота
    ytdl_options = { 
        'format' : 'bestaudio/best',
        'postprocessors' : [{
            'key' : 'FFmpegExtractAudio',
            'preferredcodec' : 'mp3', # кодек
            'preferredquality' : '192' # битрейт
        }],
    }

    with youtube_dl.YoutubeDL(ytdl_options) as ydl:
        ydl.download([url]) 

    for file in os.listdir('./'): # проверяет файлы в корне директории бота
        if file.endswith('mp3'): # если файл заканчивается на mp3
            name = file 
            os.rename(file, 'song.mp3') # заменяет название файла на song.mp3
    voice.play(discord.FFmpegPCMAudio('song.mp3')) # запускает проигрывание song.mp3 через ffmpeg
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07 # == 100% громкости

    song_name = name.rsplit('-', 2)
    await ctx.send(f'Сейчас играет: {song_name[0]}')

# команда остановки воспроизведения и выхода из канала
@bot.command(pass_context=True)
async def stop(ctx):
    voice = get (bot.voice_clients, guild = ctx.guild)
    voice.stop()
    if voice and voice.is_connected():
        await voice.disconnect()


@bot.command()
async def choice(ctx, *args):  #*args значит несколько слов))))
    pomoika = []
    urlYT = 'https://www.youtube.com/results?search_query='
    for i in args:
        urlYT = urlYT + i + '+' # соединяем ссылку со словами, получается норм ссылка

    req = requests.get(urlYT, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(req.text, "html.parser")


    for item in soup.select("html body div h3"): # поиск по CSS селекторам, на ютубе под 3 заголовком норм инфа (название + href)
        if item.find('a') == None:               #деюил находит три None а(англ) тэга
            continue
        pomoika.append(item.find('a').get('href') + '  ' + item.find('a').get('title')) # в кучу фигачим название + href, получается в 1 штуке сразу и название, и ссылка
        # [/watch?v=Fwxpmsr8PRA  ЛУЧШИЕ ПРИКОЛЫ 2020 Апрель #112 ржака угар ПРИКОЛЮХА, '/watch?v=n1NBTA6t0D0  ЛУЧШИЕ ПРИКОЛЫ 2020 Январь #75 ржака угар ПРИКОХА' и т.д
        # если сделать pomoika[0], то получим /watch?v=Fwxpmsr8PRA  ЛУЧШИЕ ПРИКОЛЫ 2020 Апрель #112 ржака угар ПРИКОЛЮХА сразу вмести, поэтому я хотел в словарь