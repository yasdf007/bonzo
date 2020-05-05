# created by /bonzo/ team

# необходимое каждому модулю команд начало
from bonzoboot import bot

# импорт дополнительных модулей
from bs4 import BeautifulSoup
import requests
import youtube_dl
from discord.utils import get
import os
import discord

# функция проигрывания музыки
async def rock(ctx, url: str):

    directory = "./"

    files_in_directory = os.listdir(directory)
    filtered_files = [file for file in files_in_directory if file.endswith(".mp3")]
    for file in filtered_files:
    	path_to_file = os.path.join(directory, file)
    	os.remove(path_to_file)
  
    voice = get (bot.voice_clients, guild = ctx.guild) # получает список голосовых соединений бота
    channel = ctx.message.author.voice.channel

    if voice and voice.is_connected():
        await voice.move_to(channel)
        del(voice)
    else:
        await channel.connect()
        del(voice)

    await ctx.send("достаю этот трек из помойки...")

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

    voice.play(discord.FFmpegPCMAudio(name)) # запускает проигрывание song.mp3 через ffmpeg
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07 # == 100% громкости

    await ctx.send(f'сейчас играет: {name}')

# функция выбора из поиска по youtube
async def choice(ctx, arges):  #*args значит несколько слов))))
    url = ''
    url_title_DICT = {}
    max_URL = 0
    urlYT = 'https://www.youtube.com/results?search_query='
    for i in arges:
        urlYT = urlYT + i + '+' # соединяем ссылку со словами, получается норм ссылка

    await discord.TextChannel.purge(ctx.message.channel, limit=1)

    req = requests.get(urlYT, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(req.text, "html.parser")

    for item in soup.select("html body div h3"): # поиск по CSS селекторам, на ютубе под 3 заголовком норм инфа (название + href)
        if item.find('a') == None:               #деюил находит три None а(англ) тэга
            continue

        url_title_DICT[(item.find('a').get('title'))] = (item.find('a').get('href'))
        max_URL +=1
        if max_URL == 5:
            break

    values = list(url_title_DICT.values())

    embed = discord.Embed(
        title = '**Выбирай чё сыграть**',
        colour = 0xcf0cc5 )
    embed.set_thumbnail(url='https://media.discordapp.net/attachments/681179689775398943/701429887470403655/unknown.png?size=256')
    embed.set_footer(text="/by bonzo/ for @" + ctx.message.author.name)

    number = 1
    for key in url_title_DICT.keys():
        embed.add_field(name='**' + str(number) + '.' + '**', value=key, inline=False)
        number+=1

    await ctx.send(embed=embed) # высрать топ 5 по поиску

    choice = await bot.wait_for('message')
    a = choice.content

    if a == str(1) or a == str(2) or a == str(3) or a == str(4) or a == str(5):
        if a == str(1):
            url = 'https://www.youtube.com' + values[0]

        if a == str(2):
            url = 'https://www.youtube.com' + values[1]

        if a == str(3):
            url = 'https://www.youtube.com' + values[2]

        if a == str(4):
            url = 'https://www.youtube.com' + values[3]

        if a == str(5):
            url = 'https://www.youtube.com' + values[4]

        await rock(ctx, url)
    else:
        await ctx.send('Ты нихуя не выбрал = ты **пошёл нахуй** (нахуя ты вообще просил......)')

# команда запуска воспроизведения по ссылке или по запросу
@bot.command(pass_context=True)
async def play(ctx, *args): # функция play принимает контекст (вызвана из дискорда) и множество аргументов (тип tuple с которым нереально работать)
    arges = list(args) # превращаем *args тапл в лист arges
    if arges[0].startswith('http'): # проверяем, ссылка ли отправлена (начинаются ли поданные *args с http)
        url = arges[0] # да? значит, единственный объект (0) => это наша ссылка
        await rock(ctx, url) # вызываем rock в этом же контексте (как будто её вызвал пользователь), аргумент - ссылка из url
    else:
        await choice(ctx, arges) # иначе, вызываем choice с аргументом arges (список слов)

# команда остановки воспроизведения и выхода из канала
@bot.command(pass_context=True)
async def stop(ctx):
    voice = get (bot.voice_clients, guild = ctx.guild)
    voice.stop()
    if voice and voice.is_connected():
        await voice.disconnect()
    await discord.TextChannel.purge(ctx.message.channel, limit=1)
    await ctx.send('пон, ливаю')
