"""
Created by ムAloneStranger (c) 2023.
файл-загрузчик бота.
осуществлять запуск только из этого файла.
"""

from sys import dont_write_bytecode
dont_write_bytecode = True  # убирает генерацию машинного кода python

# IMPORT START

print("loading...")
print("-----------------------------")

import discord

from discord              import Intents, Game, Status
from discord.ext.commands import Cog, when_mentioned_or
from discord.ext.commands import Bot as bonzoBot

from config   import OWNER_IDS, prefix, DEBUG_GUILD
from database import db

from colorama import Fore, Style
from dotenv   import load_dotenv
from time     import time

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from platform import platform
from os       import listdir, getenv

import logging

from dependencies.all                      import Dependencies
from dependencies.repository.prefix.memory import PrefixRepositoryMemory
from dependencies.api.youtube_random.sdk   import YoutubeRandomApiSDK
from dependencies.api.weather.openweather  import OpenWeatherMapAPI
from dependencies.api.weather.wttr         import WttrAPI
from dependencies.api.nasa.nasa            import NasaApi
from dependencies.api.dvach.dvach          import RandomtubeAPI
from dependencies.api.crypto.coinmarketcap import CoinmarketcapAPI

from database.memory.db import DictMemoryDb

print(Fore.GREEN + "libs imported")
print("-----------------------------")
print(f"Powered on {discord.__name__} | version {discord.__version__}")
print("-----------------------------" + Fore.MAGENTA)

# IMPORT END



load_dotenv()  # загружает файл env


logger = logging.getLogger("discord").setLevel(logging.DEBUG)

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

            youtube_random_api=YoutubeRandomApiSDK(getenv("YOUTUBE_API_KEY")),
            openweather_api=OpenWeatherMapAPI(getenv("WEATHER_TOKEN")),
            crypto_api=CoinmarketcapAPI(getenv('COINMARKETCAP_API_KEY')),
            wttr_api=WttrAPI(),
            nasa_api=NasaApi(),
            dvach_api=RandomtubeAPI(),
        )

        await self.cogsLoad()

        if DEBUG_GUILD:
            self.tree.copy_global_to(guild=DEBUG_GUILD)
            await self.tree.sync(guild=DEBUG_GUILD)
        else:
            await self.tree.sync()
   
        try:
            self.pool = await db.connectToDB()
        except Exception as err:
            print(
                f"/ \n {Fore.RED} DB PASSWORD INVALID/ DB IS NOT SPECIFIED. ERRORS RELATED TO DATABASE DISRUPTION ARE NOT HANDLED YET. {Style.RESET_ALL}"
            )
            print(err)
            await self.unload_extension(f"commands.xpSystem")
            await self.unload_extension(f"commands.freeGames")

    def cogsLoad(self):
        curr, total = 1, len(listdir("./commands")) - 4 # cogs - folder

        for filename in listdir("./commands"):

            if filename.endswith(".py"):
                try: # load cog
                    self.load_extension(f"commands.{filename[:-3]}")
                    print(f"cog {filename} load, {curr}/{total}")

                except Exception as error: # something in cog wrong
                    print(f"error in cog {filename}, {curr}/{total} | {error}")
                    logging.error(f"cog filename not load: {error}")

                curr += 1 # + 1 for current amount


    async def _get_prefix(self, bot, message):
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


if __name__ == "__main__":
    bot = Bot()

    try:
        bot.run()
    except:
        print(Fore.RED +  "-----------------------\nConnection failed\n-----------------------" + Style.RESET_ALL)
    finally:
        print(Fore.YELLOW +  "-----------------------\nStopped\n-----------------------" + Style.RESET_ALL)


# events

@bot.event
async def on_resumed():
    print(Fore.GREEN +  "-----------------------\nbot resumed\n-----------------------" + Style.RESET_ALL)
    logging.info("bot resumed")


@bot.event
async def on_disconnect():
    print(Fore.RED +  "-----------------------\nbot disconnected or connection failed\n-----------------------" + Style.RESET_ALL)
    logging.warning("bot disconnected")

@bot.event
async def on_connect():
    print(Fore.GREEN +  "-----------------------\nbot connected\n-----------------------" + Style.RESET_ALL)
    logging.info("bot connected")

