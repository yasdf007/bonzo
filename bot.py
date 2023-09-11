# IMPORT START

import logging
from os import getenv
from pathlib import Path
from platform import platform
from time import time

import discord
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from colorama import Fore, Style
from discord import Game, Intents, Message, Status
from discord.ext.commands import Bot as bonzoBot
from discord.ext.commands import Cog, when_mentioned_or
from dotenv import load_dotenv

from config import OWNER_IDS, PREFIX
from dependencies.repository.prefix.abc import PrefixRepository

print("loading...")
print("-----------------------------")


print(Fore.GREEN + "libs imported")
print("-----------------------------")
print(f"Powered on {discord.__name__} | version {discord.__version__}")
print("-----------------------------" + Fore.MAGENTA)

# IMPORT END


load_dotenv()  # загружает файл env

logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)


handler = logging.FileHandler(
    filename="discord.log", encoding="utf-8", mode="a")
handler.setFormatter(
    logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)
logger.addHandler(handler)


class Bot(bonzoBot):
    def __init__(self, prefix_repo: PrefixRepository):
        intents = Intents.default()
        intents.presences = True
        intents.members = True
        # it is mandatory to request access to this intent explicitly via discord dev portal
        intents.message_content = False

        self.prefix_repo = prefix_repo

        super().__init__(
            command_prefix=self._get_prefix,
            help_command=None,
            intents=intents,
            owner_ids=OWNER_IDS,
        )

        self.game = Game("@Bonzo init | stacknox2")
        self.scheduler = AsyncIOScheduler()
        self.startTime = None

    async def setup_hook(self):
        await self.cogsLoad()

        # await self.tree.sync()

    async def cogsLoad(self):
        cmds = [x.stem for x in Path(
            './commands').iterdir() if x.suffix == '.py' and x.is_file()]
        total = len(cmds)

        for curr, cmd in enumerate(cmds, start=1):
            try:
                await self.load_extension(f"commands.{cmd}")
                print(f"cog {cmd} load, {curr}/{total}")

            except Exception as error:  # something in cog wrong
                print(f"error in cog {cmd}, {curr}/{total} | {error}")
                logging.error(f"cog filename not load: {error}")

    async def _get_prefix(self, bot, message: Message):
        if not message.guild:
            return when_mentioned_or(PREFIX)(bot, message)

        guild_prefix = await self.prefix_repo.prefix_for_guild(guild_id=message.guild.id) or PREFIX

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
        print(Fore.GREEN + "-----------------------\nbot resumed\n-----------------------" + Style.RESET_ALL)
        logging.info("bot resumed")

    @Cog.listener()
    async def on_disconnect(self):
        print(Fore.RED + "-----------------------\nbot disconnected or connection failed\n-----------------------" + Style.RESET_ALL)
        logging.warning("bot disconnected")

    @Cog.listener()
    async def on_connect(self):
        print(Fore.GREEN + "-----------------------\nbot connected\n-----------------------" + Style.RESET_ALL)
        logging.info("bot connected")
