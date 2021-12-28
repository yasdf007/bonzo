from discord import Embed
from discord.ext.commands.context import Context
from discord.ext.commands import Cog, command, CommandError
from discord_slash import SlashContext, cog_ext
from discord_slash.error import SlashCommandError
from aiohttp import ClientSession
from config import guilds
from .resources.AutomatedMessages import automata

name = "nasapict"
description = "Картинка дня от NASA"


class NoPhotoFound(CommandError, SlashCommandError):
    pass


class Nasa(Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_command_error(self, ctx, error):
        if isinstance(error, NoPhotoFound):
            return await ctx.send(
                automata.generateEmbErr("Не удалось получить картинку дня", error=error)
            )

    @Cog.listener()
    async def on_slash_command_error(self, ctx, error):
        if isinstance(error, NoPhotoFound):
            return await ctx.send(
                automata.generateEmbErr("Не удалось получить картинку дня", error=error)
            )

    @command(name=name, description=description)
    async def nasapict_prefix(self, ctx: Context):
        await self.nasapict(ctx)

    @cog_ext.cog_slash(name=name, description=description)
    async def nasapict_slash(self, ctx: SlashContext):
        await self.nasapict(ctx)

    async def nasapict(self, ctx):
        embed = Embed(title="Картинка дня от NASA", color=0x0000FF)

        query = "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY"
        async with ClientSession() as session:
            async with session.get(query) as response:
                res = await response.json()
        try:
            image = res["hdurl"]
            title = res["title"]

            embed.set_image(url=image)
            embed.set_footer(text=title)

            await ctx.send(embed=embed)
        except Exception as e:
            raise NoPhotoFound


def setup(bot):
    bot.add_cog(Nasa(bot))
