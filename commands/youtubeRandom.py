from discord.ext import commands
from googleapiclient.discovery import build
from os import getenv
from dotenv import load_dotenv
import json
from random import randint, choice
from string import digits, ascii_uppercase
load_dotenv()


class YoutubeRandom(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Обработка ошибок
    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(error)

    YOUTUBE_API_KEY = getenv('YOUTUBE_API_KEY')
    API_SERVICE_NAMCE = "youtube"
    API_VERSION = "v3"
    videoNameStart = ['IMG_']
    videoNameEnd = ['.mp4']

    # async def cog_command_error(self, ctx, error):
    #     if isinstance(error, commands.CommandOnCooldown):
    #         await ctx.send(error)

    @commands.cooldown(rate=1, per=5)
    @commands.command(name='randomVideo', description='Рандомны видос из ютуба (BETA)', aliases=['randvid', 'video'])
    async def randomVideo(self, ctx):
        # Делаем рандомное название запроса из 4 символов и цифр
        query2 = ''.join(choice(ascii_uppercase + digits) for _ in range(4))
        youtubeVideoId = ''

        #
        youtube = build(
            self.API_SERVICE_NAMCE, self.API_VERSION, developerKey=self.YOUTUBE_API_KEY
        )

        # Ищем в ютубе
        request = youtube.search().list(
            q=query2,
            maxResults=25,
            part='id'
        ).execute()

        # JSON
        requestJSON = json.loads(json.dumps(request))

        # Для каждого результата
        for searchResult in requestJSON['items']:
            # Выбираем видос (может быть плейлист, но нужен видос)
            if searchResult['id']['kind'] == 'youtube#video':
                # Сохраняем ID видоса
                youtubeVideoId = searchResult['id']['videoId']

        await ctx.send(f'https://www.youtube.com/watch?v={youtubeVideoId}')


def setup(bot):
    bot.add_cog(YoutubeRandom(bot))
