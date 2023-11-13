from discord import app_commands, Interaction
from discord.ext.commands import Cog, GroupCog
from bot import Bot
import random
from string import ascii_lowercase, digits
from aiohttp import ClientSession

from dependencies.api import youtube, dvach
from config import YOUTUBE_API_KEY

def get_random_prntsc_link():
    symbolsStr = "".join(random.choices(ascii_lowercase + digits, k=6))
    return f"https://prnt.sc/{symbolsStr}"

async def get_random_imgur_link():
        url = "https://i.imgur.com/"
        symbols = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

        i = 0
        while True:
            # 5 попыток найти картинку
            if i == 5:
                return None
            randSymbols = "".join(random.sample(symbols, 5))
            iImgurUrl = url + randSymbols + ".png"

            async with ClientSession() as session:
                async with session.head(iImgurUrl) as response:
                    if not response.headers["content-length"] == "0":
                        return iImgurUrl
                    
            i +=1


class Random(GroupCog, group_name='random', group_description='Различные случайные данные'):
    def __init__(self, bot, youtube_sdk: youtube.YoutubeRandomApiSDK, random_tube: dvach.RandomtubeAPI):
        self.bot: Bot = bot
        self.random_tube = random_tube
        self.youtube_sdk = youtube_sdk

    @app_commands.command(name='cat', description='Отправляет случайного кота')
    async def random_cat(self, inter: Interaction):
        await inter.response.send_message("https://cataas.com/cat")
    
    @app_commands.command(name='prntsc', description='Отправляет случайное изображение из https://prnt.sc')
    async def random_prntsc(self, inter: Interaction):
        await inter.response.send_message(get_random_prntsc_link())
    
    @app_commands.command(name='youtube', description='Отправляет случайное видео из https://youtube.com')
    async def random_yt(self, inter: Interaction):
        link = await self.youtube_sdk.get_random_video()
        await inter.response.send_message(link) 
    
    @app_commands.command(name='2ch', description='(18+) Отправляет случайное видео с https://2ch.hk')
    async def random_2ch(self, inter: Interaction):
        link = await self.random_tube.get_random_url()
        await inter.response.send_message(link) 

    @app_commands.command(name='imgur', description='Отправляет случайное изображение из https://imgur.com')
    async def random_imgur(self, inter: Interaction):
        link = await get_random_imgur_link()
        if not link:
            return
        await inter.response.send_message(link)

async def setup(bot):
    yt_sdk = youtube.YoutubeRandomApiSDK(YOUTUBE_API_KEY)
    random_tube = dvach.RandomtubeAPI()
    await bot.add_cog(Random(bot, yt_sdk, random_tube))
