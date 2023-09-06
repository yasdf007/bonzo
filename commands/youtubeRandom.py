from discord.ext.commands import Cog, hybrid_command, Context
from bot import Bot

from dependencies.api import youtube

from config import YOUTUBE_API_KEY

name = "randomvideo"
description = "Рандомный видос из ютуба (BETA)"

class YoutubeRandom(Cog):
    def __init__(self, bot, youtube_sdk: youtube.YoutubeRandomApiSDK):
        self.bot: Bot = bot
        self.youtube_sdk = youtube_sdk

    @hybrid_command(name=name, description=description, aliases=["randvid", "video"])
    async def randomVideo(self, ctx: Context):
        youtubeVideoId = await self.youtube_sdk.get_video_id()

        await ctx.send(f"https://www.youtube.com/watch?v={youtubeVideoId}")

async def setup(bot):
    sdk = youtube.YoutubeRandomApiSDK(YOUTUBE_API_KEY)
    await bot.add_cog(YoutubeRandom(bot, sdk))
