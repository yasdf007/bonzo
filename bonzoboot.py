# Created by ムAloneStranger (c) 2020.
# файл-загрузчик бота.
# осуществлять запуск только из этого файла.

import discord
from discord.ext import commands

import platform
from time import time

# для безопасного импорта токена
import os 
from dotenv import load_dotenv 
load_dotenv() # загружает файл env

game = discord.Game("v0.6.0 neuvo") # пишем боту в активити
bot = commands.Bot(command_prefix='bd/', help_command=None) # лёгкая референс-комманда для нашего бота, задаём префикс и встроенную команду help 

# функция запуска (можно узнать разницу между прочитыванием кода компьютером и связью с discord api)
def bonzo():
    global ctimest # переменная, содержащая разницу между временем прочтения кода и готовым к работе ботом
    ctimest = time() # таймштамп: код успешно прочитан
    print('/', 'initialization file has been successfully read. starting up bonzo...', sep='\n')
    extensions = ['commands.vlanerCog', 'commands.aloneCog', 'commands.nohameCog']
    for ext in extensions:
        bot.load_extension(ext)
    bot.run(os.getenv('TOKEN')) # берёт переменную TOKEN из .env



# on_ready выполняется при полной готовности бота к действиям
@bot.event 
async def on_ready():
    global ctimest # переменная, содержащая разницу между временем прочтения кода и готовым к работе ботом
    await bot.change_presence(status=discord.Status.online, activity=game) # бот меняет свой статус именно благодаря этой команде (и "играет" в "игру" которую мы задали в строке 13)
    ctimest = time() - ctimest # дельта времени: бот готов к работе
    print('/', 'bonzo has been successfully initialized on ' + platform.platform(), 'timestamp delta is: ' + str(round(ctimest,3)) + 's', 'discord latency is: ' + str(round(bot.latency, 3)) + 's', '/', sep='\n')
# #    if not discord.opus.is_loaded():
# #        discord.opus.load_opus('opus')



# запускаем инстанцию бота
bonzo()
