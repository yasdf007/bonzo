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
load_dotenv()  # загружает файл env

game = discord.Game("0.7.4 neuvo")  # пишем боту в активити
# лёгкая референс-комманда для нашего бота, задаём префикс и встроенную команду help
bot = commands.Bot(command_prefix=str(os.getenv('PREFIX')), help_command=None)


# функция запуска (можно узнать разницу между прочитыванием кода компьютером и связью с discord api)
def main():
    global ctimest  # переменная, содержащая разницу между временем прочтения кода и готовым к работе ботом
    ctimest = time()  # таймштамп: код успешно прочитан
    print('/', 'initialization file has been successfully read. starting up bonzo...', sep='\n')

    bot.run(os.getenv('TOKEN'))  # берёт переменную TOKEN из .env

# on_ready выполняется при полной готовности бота к действиям


@bot.event
async def on_ready():
    # бот меняет свой статус именно благодаря этой команде (и "играет" в "игру")
    await bot.change_presence(status=discord.Status.online, activity=game)
    endTime = time() - ctimest
    extensions = ['commands.vlanerCog',
                  'commands.aloneCog',
                  'commands.nohameCog',
                  'commands.musicCog']
    for ext in extensions:
        bot.load_extension(ext)
    print('/', 'bonzo has been successfully initialized on ' + platform.platform(), 'timestamp delta is: ' +
          str(round(endTime, 3)) + 's', 'discord latency is: ' + str(round(bot.latency, 3)) + 's', '/', sep='\n')


# запускаем инстанцию бота
if (__name__ == '__main__'):
    main()
