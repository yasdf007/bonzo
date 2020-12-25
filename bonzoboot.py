# Created by ムAloneStranger (c) 2020.
# файл-загрузчик бота.
# осуществлять запуск только из этого файла.
from discord import Intents, Game, Status
from discord.ext.commands import Bot as bonzoBot, Cog
from platform import platform
from time import time
from os import listdir, getenv
from dotenv import load_dotenv

load_dotenv()  # загружает файл env


class Bot(bonzoBot):
    def __init__(self):
        intents = Intents.all()
        self.game = Game("b/help | v1.0 RC2")
        self.startTime = None
        self.guild = None

        super().__init__(command_prefix=getenv('PREFIX'),
                         help_command=None, intents=intents)

    def cogsLoad(self):
        for filename in listdir('./commands'):
            if filename.endswith('.py') and not filename.startswith('music'):
                self.load_extension(f'commands.{filename[:-3]}')
                print(f'loaded {filename}')

    def run(self):
        self.startTime = time()  # таймштамп: код успешно прочитан
        print('/', 'initialization file has been successfully read. starting up bonzo...', sep='\n')
        self.cogsLoad()
        super().run(getenv('TOKEN'))  # берёт переменную TOKEN из .env

    @Cog.listener()
    async def on_ready(self):

        self.guild = self.get_guild(664485208745050112)
        # бот меняет свой статус именно благодаря этой команде (и "играет" в "игру")
        await self.change_presence(status=Status.online, activity=self.game)
        self.load_extension('commands.music')

        endTime = time() - self.startTime

        print(
            f'/ \n bonzo has been successfully initialized on {platform()} \n timestamp delta is: {round(endTime, 3)}s \n discord latency is: {(round(self.latency, 3))}s \n /')


bot = Bot()
bot.run()
