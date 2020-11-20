from discord.ext import commands
from googleapiclient.discovery import build
from os import getenv
from dotenv import load_dotenv
import json
from random import randint, choice
load_dotenv()


class YoutubeRandom(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
    @commands.command()
    async def randomVideo(self, ctx):
        youtube = build(
            self.API_SERVICE_NAMCE, self.API_VERSION, developerKey=self.YOUTUBE_API_KEY
        )

        query = choice(self.videoNameStart) + \
            str(randint(1, 9999)) + choice(self.videoNameEnd)
        request = youtube.search().list(
            q=query,
            maxResults=25,
            part='id'
        ).execute()

        requestJSON = json.loads(json.dumps(request))
        totalResults = (requestJSON['pageInfo']['totalResults'] % 25) - 1
        youtubeVideoId = requestJSON['items'][totalResults]['id']['videoId']
        await ctx.send(f'https://www.youtube.com/watch?v={youtubeVideoId}')


def setup(bot):
    bot.add_cog(YoutubeRandom(bot))
