from os import getenv
from dotenv import load_dotenv
from discord import Object

load_dotenv()

DEBUG_GUILD = Object(id=int(getenv("DEBUG_GUILD")))
MAIN_GUILD = Object(id=int(getenv("MAIN_GUILD")))

OWNER_IDS = [int(id) for id in getenv("OWNER_IDS").split(",") if len(getenv("OWNER_IDS")) > 0] or []

PREFIX = getenv("PREFIX") or "b/"

LAVALINK_HOST=getenv('LAVALINK_HOST')
LAVALINK_PORT=int(getenv('LAVALINK_PORT'))
LAVALINK_NODE_PASSWORD=getenv('LAVALINK_NODE_PASSWORD')

LAVALINK_CONNECTION_OPTIONS={'host': LAVALINK_HOST, 'port': LAVALINK_PORT, 'password': LAVALINK_NODE_PASSWORD, 'identifier': 'MAIN'}

YOUTUBE_API_KEY=getenv('YOUTUBE_API_KEY')
COINMARKETCAP_API_KEY=getenv('COINMARKETCAP_API_KEY')

def not_empty(**kwargs):
    for k, v in kwargs.items():
        if not v:
            raise TypeError(f"ARGUMENT **{k}** MUST NOT BE EMPTY")
        
not_empty(MAIN_GUILD=MAIN_GUILD, PREFIX=PREFIX)