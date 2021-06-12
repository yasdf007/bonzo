# Created by ムAloneStranger (c) 2020.
# файл-загрузчик бота.
# осуществлять запуск только из этого файла.

from colorama import Fore, Back, Style
from dotenv import load_dotenv
from database import db
from os import listdir, getenv
from time import time
from platform import platform
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext.commands import Bot as bonzoBot, Cog, when_mentioned_or
from discord import Intents, Game, Status
import sys
sys.dont_write_bytecode = True  # убирает генерацию машинного кода python

load_dotenv()  # загружает файл env
OWNER_IDS = [int(id) for id in getenv('OWNER_IDS').split(',')]


class Bot(bonzoBot):
    def __init__(self):
        sys.dont_write_bytecode = True
        intents = Intents.all()
        self.game = Game("b/help | v1.0 RC GM")
        self.scheduler = AsyncIOScheduler()
        self.startTime = None
        super().__init__(command_prefix=when_mentioned_or(getenv('PREFIX')),
                         help_command=None, intents=intents, owner_ids=OWNER_IDS)

    def cogsLoad(self):
        curr, total = 0, len(listdir('./commands')) - 3
        for filename in listdir('./commands'):
            if filename.endswith('.py') and not filename.startswith('music'):
                self.load_extension(f'commands.{filename[:-3]}')
                curr += 1
                print(f'loaded {filename}, {curr}/{total}')
        print(Back.WHITE + Fore.BLACK +
              "MUSIC WAS TEMPORARILY REMOVED FROM BONZO DUE TO HOSTING ISSUES" + Style.RESET_ALL)

    def run(self):
        self.startTime = time()  # таймштамп: код успешно прочитан
        print('/', 'initialization file has been successfully read. starting up bonzo...', sep='\n')
        self.cogsLoad()
        super().run(getenv('TOKEN'))  # берёт переменную TOKEN из .env

    @Cog.listener()
    async def on_ready(self):
        self.pool = await db.connectToDB()

        # бот меняет свой статус именно благодаря этой команде (и "играет" в "игру")
        await self.change_presence(status=Status.online, activity=self.game)
        # self.load_extension('commands.music')
        self.scheduler.start()

        endTime = time() - self.startTime

        print(
            f'/ \n bonzo has been successfully initialized on {platform()} \n timestamp delta is: {round(endTime, 3)}s \n discord latency is: {(round(self.latency, 3))}s \n / \n end.')


bot = Bot()
bot.run()
