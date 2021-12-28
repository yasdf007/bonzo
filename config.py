from os import getenv
from dotenv import load_dotenv
from colorama import Fore, Back, Style

load_dotenv()

guilds = None
try:
    OWNER_IDS = [int(id) for id in getenv("OWNER_IDS").split(",")]
except:
    OWNER_IDS = None
    print(f"{Fore.GREEN} Config: {Style.RESET_ALL} Owners unspecified.")

if not len(getenv("PREFIX")) == 0:
    prefix = getenv("PREFIX")
else:
    prefix = "b/"
    print(
        f"{Fore.GREEN} Config: {Style.RESET_ALL} Prefix unspecified. Using default prefix {prefix}."
    )
