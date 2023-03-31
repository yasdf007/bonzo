from discord.ext.commands import Cog, command, hybrid_command
from discord.ext.commands.context import Context
from repository.youtube_random.abc import YoutubeRandomRepository


name = "randomvideo"
description = "Рандомный видос из ютуба (BETA)"

class YoutubeRandom(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.youtube_random_repo: YoutubeRandomRepository = self.bot.repos.youtube_random_repo

    async def cog_command_error(self, ctx, error):
        raise error
        
    @hybrid_command(name=name, description=description, aliases=["randvid", "video"])
    async def randomVideo(self, ctx):
        youtubeVideoId = await self.youtube_random_repo.get_video_id()

        await ctx.send(f"https://www.youtube.com/watch?v={youtubeVideoId}")

async def setup(bot):
    await bot.add_cog(YoutubeRandom(bot))
