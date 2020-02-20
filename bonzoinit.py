# Created by ムAloneStranger (c) 2020.
# ver 0
# !любые запуски производить строго из этого файла!
# на первое время можно поэксперементировать с добавлением функционала здесь, между ивентом запуска (закомментирован) и запуском самой инстанции
# но будет лучше если мы как можно скорее сможем разработать модульную конструкцию (события хранятся в отдельном файле и импортируются сюда), чтобы было проще 
# 1) разделить код по авторам 2) понимать, где что находится и удобно редактировать функции 3) не использовать один файл бесконечной длины.

import platform
from discord.ext import commands
from authvar import token

bot = commands.Bot(command_prefix='b/')

@bot.event
async def on_ready():
    print('/', 'bonzo has been successfully initialized on ' + platform.platform(), '/', sep='\n')

bot.run(token)