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
load_dotenv() 

game = discord.Game("v0.3.2 rocescrite") # пишем боту в активити
bot = commands.Bot(command_prefix='b/', help_command=None)

# функция запуска (можно узнать разницу между прочитыванием кода компьютером и связью с discord api)
def bonzo():
    global ctimest
    ctimest = time() # таймштамп: код успешно прочитан
    print('/', 'initialization file has been successfully read. starting up bonzo...', sep='\n')
    bot.run(os.getenv('TOKEN'))

# eval - запуск кода от лица бота овнером через discord.
@bot.command() 
async def evala(ctx, evcode=None):
    ownerids = [221246477630963722, 196314341572608000, 393807398047055883] # определяем овнеров
    if evcode == None: # проверяем, указан ли код
        await ctx.send("укажите код для экзекьюции.")
    else:
        if ctx.author.id in ownerids: # проверяем, овнер ли запросил команду?
            execute = eval(str(evcode))
            await execute
        else: 
            await ctx.send("ты бесправное чмо " + '{0.author.mention}'.format(ctx))

# импорт файла-фикса для импорта наших функций
from botlib.blankfix import * 

# импорт наших собственных функций в файл инстанции.
from botlib.func_nohame import *
from botlib.func_alone import *
from botlib.func_vlaner import *

# on_ready выполняется при полной готовности бота к действиям
@bot.event 
async def on_ready():
    global ctimest
    await bot.change_presence(status=discord.Status.online, activity=game) # бот меняет свой статус именно благодаря этой команде (и "играет" в "игру" которую мы задали в строке 13)
    ctimest = time() - ctimest # дельта времени: бот готов к работе
    print('/', 'bonzo has been successfully initialized on ' + platform.platform(), 'timestamp delta is: ' + str(round(ctimest,3)) + 's', 'discord latency is: ' + str(round(bot.latency, 3)) + 's', '/', sep='\n')

# запускаем инстанцию бота
bonzo()
