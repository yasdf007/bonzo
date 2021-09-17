from os import getenv
from dotenv import load_dotenv

load_dotenv()

guilds = None
OWNER_IDS = [int(id) for id in getenv('OWNER_IDS').split(',')]
prefix ="b/"
