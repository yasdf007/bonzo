from os import getenv
from dotenv import load_dotenv

load_dotenv()

guilds = [664485208745050112]
OWNER_IDS = [int(id) for id in getenv('OWNER_IDS').split(',')]
prefix ="b/"
