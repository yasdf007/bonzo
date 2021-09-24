# Created by ムAloneStranger (c) 2020.
# файл-загрузчик бота.
# осуществлять запуск только из этого файла.

from sys import dont_write_bytecode
dont_write_bytecode = True # убирает генерацию машинного кода python

from discord.ext.commands import Bot as bonzoBot, Cog, when_mentioned_or
from discord import Intents, Game, Status
from discord_slash import SlashCommand

from config import OWNER_IDS, prefix

from colorama import Fore, Back, Style
from dotenv import load_dotenv
from database import db
from time import time
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from platform import platform
from os import listdir, getenv
import logging

load_dotenv()  # загружает файл env

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)

handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w'
)
handler.setFormatter(
    logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s')
)
logger.addHandler(handler)


class Bot(bonzoBot):
    def __init__(self):
        intents = Intents.all()
        self.game = Game(f'{prefix}help | v1.11a okshaw')
        self.scheduler = AsyncIOScheduler()
        self.startTime = None
        super().__init__(command_prefix=when_mentioned_or(prefix),
                         help_command=None, intents=intents, owner_ids=OWNER_IDS)

    def cogsLoad(self):
        curr, total = 0, len(listdir('./commands')) - 2
        for filename in listdir('./commands'):
            if filename.endswith('.py'):
                if not filename == 'music.py':
                    self.load_extension(f'commands.{filename[:-3]}')

                    curr += 1
                    print(f'loaded {filename}, {curr}/{total}')

                elif filename.startswith('music'):
                        print(
                            f'/ \n {Fore.GREEN}MUSIC MODULE HAS BEEN SUCCESFULLY INITIALIZED. {Style.RESET_ALL} \n{curr}/{total} \n/')
                        curr += 1

    def run(self):
        self.startTime = time()  # таймштамп: код успешно прочитан
        print('/', 'initialization file has been successfully read. starting up bonzo...', sep='\n')
        self.cogsLoad()
        super().run(getenv('TOKEN'))  # берёт переменную TOKEN из .env

    @Cog.listener()
    async def on_ready(self):
        try:
            self.pool = await db.connectToDB()
        except Exception as err:
            print(f"/ \n {Fore.RED} DB PASSWORD INVALID/ DB IS NOT SPECIFIED. ERRORS RELATED TO DATABASE DISRUPTION ARE NOT HANDLED YET. {Style.RESET_ALL}")
            print(err)

        # бот меняет свой статус именно благодаря этой команде (и "играет" в "игру")
        await self.change_presence(status=Status.online, activity=self.game)

        self.scheduler.start()
        endTime = time() - self.startTime

        print(
            f'/ \n bonzo has been successfully initialized on {platform()} \n timestamp delta is: {round(endTime, 3)}s \n discord latency is: {(round(self.latency, 3))}s \n / \n end.')


if __name__ == '__main__':
    try:
        bot = Bot()
        slash = SlashCommand(bot, sync_commands=True)
        bot.slash = slash
        bot.run()
    except Exception as error:
        print("FATAL ERROR. \n THIS ERROR CAN OCCUR EITHER IF MAIN BOT EXECUTABLE IS CORRUPTED OR IF FRAMEWORK IS BROKEN.")
        print(error)
