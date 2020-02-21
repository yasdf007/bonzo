# Created by ムAloneStranger (c) 2020.
# ver 0.0.(0).2 propheader

# ! ПРОШУ НЕ ВНОСИТЬ НИКАКИХ ИЗМЕНЕНИЙ В ЭТОТ ФАЙЛ !

# осуществлять запуск бота из этого файла.

import platform # необходимо для считывания версии системы 
import discord # здесь нам пригодятся вообще в принципе функции api дискорда (для статуса бота например)
from discord.ext import commands # импортируем саму библиотеку api *бота* для дискорда
from authvar import token # токен из нашего второго файла берём

game = discord.Game("v0.0.(0).2 propheader") # типо пишем боту в активити че он делает))0
bot = commands.Bot(command_prefix='b/') # чтобы не писать везде что это commands.Bot и префикс, мы просто делаем переменную и рубим profit

def bonzo(): # функция запуска (можно узнать разницу между прочитыванием кода компьютером и связью с discord api)
    print('/', 'initialization file has been successfully read. starting up bonzo...', '/', sep='\n')
    bot.run(token)

# импорт наших собственных функций в файл инстанции.
from botlib.func_alone import *
from botlib.func_vlaner import *
from botlib.func_nohame import *

@bot.event # on_ready выполняется при полной готовности бота к действиям
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=game) # бот меняет свой статус именно благодаря этой команды (и "играет" в "игру" которую мы задали в строке 13)
    print('/', 'bonzo has been successfully initialized on ' + platform.platform(), '/', sep='\n')

bonzo() # запускаем !
