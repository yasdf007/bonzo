# IMPORT START

print("loading...")
print("-----------------------------")

import discord
import json

from discord              import Intents, Game, Status, Message
from discord.ext.commands import Cog, when_mentioned_or, Bot as bonzoBot

from commands.resources.AutomatedMessages import AutoEmbed
from config                               import OWNER_IDS, prefix

from colorama import Fore, Style
from dotenv   import load_dotenv
from time     import time

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from platform import platform
from os       import getenv
from pathlib import Path


import logging

from dependencies.all                           import Dependencies

from dependencies.repository.prefix.memory      import PrefixRepositoryMemory
from dependencies.repository.free_games.memory  import FreeGamesRepositoryMemory
from dependencies.repository.member_info.memory import MemberHandlerRepositoryMemory

from dependencies.api.youtube_random.sdk        import YoutubeRandomApiSDK
from dependencies.api.weather.openweather       import OpenWeatherMapAPI
from dependencies.api.weather.wttr              import WttrAPI
from dependencies.api.nasa.nasa                 import NasaApi
from dependencies.api.dvach.dvach               import RandomtubeAPI
from dependencies.api.crypto.coinmarketcap      import CoinmarketcapAPI
from dependencies.api.free_games.epic_games     import EpicGamesApi

from database.memory.db import DictMemoryDb

print(Fore.GREEN + "libs imported")
print("-----------------------------")
print(f"Powered on {discord.__name__} | version {discord.__version__}")
print("-----------------------------" + Fore.MAGENTA)

# IMPORT END


error_dict = json.load(open("errors.json", "r"))


load_dotenv()  # загружает файл env

autoemb = AutoEmbed()

logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)


handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
handler.setFormatter(
    logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)
logger.addHandler(handler)


class Bot(bonzoBot):
    def __init__(self):
        intents = Intents.default()
        intents.members = True
        intents.message_content = True

        super().__init__(
            command_prefix=self._get_prefix,
            help_command=None,
            intents=intents,
            owner_ids=OWNER_IDS,
        )

        self.game = Game(f"@Bonzo init | stacknox2")
        self.scheduler = AsyncIOScheduler()
        self.startTime = None
    
    async def setup_hook(self):
        mem = DictMemoryDb
        
        self.dependency = Dependencies(
            prefix_repo=PrefixRepositoryMemory(mem),
            free_games_repo=FreeGamesRepositoryMemory(mem),
            members_repo=MemberHandlerRepositoryMemory(mem),
            youtube_random_api=YoutubeRandomApiSDK(getenv("YOUTUBE_API_KEY")),
            openweather_api=OpenWeatherMapAPI(getenv("WEATHER_TOKEN")),
            crypto_api=CoinmarketcapAPI(getenv('COINMARKETCAP_API_KEY')),
            wttr_api=WttrAPI(),
            nasa_api=NasaApi(),
            dvach_api=RandomtubeAPI(),
            free_games_api=EpicGamesApi(),
        )

        await self.cogsLoad()

        # await self.tree.sync()

    async def cogsLoad(self):
        cmds = [x.stem for x in Path('./commands').iterdir() if x.suffix == '.py' and x.is_file()]
        total = len(cmds)

        for curr, cmd in enumerate(cmds, start=1):
            try:
                await self.load_extension(f"commands.{cmd}")
                print(f"cog {cmd} load, {curr}/{total}")

            except Exception as error: # something in cog wrong
                print(f"error in cog {cmd}, {curr}/{total} | {error}")
                logging.error(f"cog filename not load: {error}")


    async def _get_prefix(self, bot, message: Message):
        if not message.guild:
            return when_mentioned_or(prefix)(bot, message)
        
        guild_prefix = await self.dependency.prefix_repo.prefix_for_guild(guild_id=message.guild.id) or prefix

        return when_mentioned_or(guild_prefix)(bot, message)

    def run(self):
        self.startTime = time()  # таймштамп: код успешно прочитан
        print(
            "/",
            "initialization file has been successfully read. starting up bonzo...",
            sep="\n",
        )
        super().run(getenv("TOKEN"))  # берёт переменную TOKEN из .env

    @Cog.listener()
    async def on_ready(self):
        # бот меняет свой статус именно благодаря этой команде (и "играет" в "игру")
        await self.change_presence(status=Status.online, activity=self.game)

        self.scheduler.start()
        endTime = time() - self.startTime

        print(
            f"/ \n bonzo has been successfully initialized on {platform()} \n timestamp delta is: {round(endTime, 3)}s \n discord latency is: {(round(self.latency, 3))}s \n / \n end."
        )

    @Cog.listener()
    async def on_resumed(self):
        print(Fore.GREEN +  "-----------------------\nbot resumed\n-----------------------" + Style.RESET_ALL)
        logging.info("bot resumed")

    @Cog.listener()
    async def on_disconnect(self):
        print(Fore.RED +  "-----------------------\nbot disconnected or connection failed\n-----------------------" + Style.RESET_ALL)
        logging.warning("bot disconnected")

    @Cog.listener()
    async def on_connect(self):
        print(Fore.GREEN +  "-----------------------\nbot connected\n-----------------------" + Style.RESET_ALL)
        logging.info("bot connected")



    @Cog.listener()
    async def on_slash_command_error(ctx, error):
        await ctx.send(
            embed=AutoEmbed.type_autoembed(
            "error",
            f"```{error_dict[error.__class__.__name__]}```"
            ),
            ephemeral=True,
        components=[
            discord.ui.Button(
            style=discord.ButtonStyle.url, 
            label="репортнуть", 
            url="https://discord.gg/ZNrSmQfp2d"
            )
            ]
        )
