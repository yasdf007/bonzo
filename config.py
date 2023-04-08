from os import getenv
from dotenv import load_dotenv
from colorama import Fore, Back, Style
from discord import Object
from dataclasses import dataclass

load_dotenv()
DEBUG_GUILD = None

if getenv("DEBUG_GUILD"):
    DEBUG_GUILD = Object(id=int(getenv("DEBUG_GUILD")))

try:
    OWNER_IDS = [int(id) for id in getenv("OWNER_IDS").split(",")]
except:
    OWNER_IDS = None
    print(f"{Fore.GREEN} Config: {Style.RESET_ALL} Owners unspecified.")

prefix = "b/"

if not len(getenv("PREFIX")) == 0:
    prefix = getenv("PREFIX")
else:
    prefix = "b/"
    print(
        f"{Fore.GREEN} Config: {Style.RESET_ALL} Prefix unspecified. Using default prefix {prefix}."
    )

@dataclass
class LavalinkConfig():
    host:str
    port:str
    password: str


lavalink_config = LavalinkConfig(
    host=getenv('LAVALINK_HOST'),
    port=getenv('LAVALINK_PORT'),
    password=getenv('LAVALINK_NODE_PASSWORD')
)