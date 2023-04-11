from discord.ext.commands import (
    Cog,
    guild_only,
    has_permissions,
    bot_has_permissions,
    BucketType,
    cooldown,
)
from apscheduler.triggers.cron import CronTrigger
from asyncio import sleep
from discord.ext.commands import hybrid_group, hybrid_command, Context, check
from discord.ext.commands.core import is_owner
from discord.ext.commands.errors import (
    CommandOnCooldown,
    MissingPermissions,
    NoPrivateMessage,
    NotOwner
)
from discord.enums import ChannelType
from discord import Embed
from discord import Colour
from discord.app_commands import guilds
from .resources.AutomatedMessages import automata

from dependencies.api.free_games.abc import FreeGamesAPI
from dependencies.repository.free_games.abc import FreeGamesRepository
from bot import Bot
from config import MAIN_GUILD

class FreeGames(Cog):
    def __init__(self, bot):
        self.bot: Bot = bot
        self.free_games_api: FreeGamesAPI = self.bot.dependency.free_games_api
        self.free_games_repo: FreeGamesRepository = self.bot.dependency.free_games_repo

        self.bot.scheduler.add_job(
            self.freeGames,
            CronTrigger(day_of_week="thu", hour=19, minute=3, jitter=120),
        )
    async def cog_command_error(self, ctx: Context, error):
        if isinstance(error, CommandOnCooldown):
            return await ctx.message.reply(
                embed=automata.generateEmbErr(
                    "Спам командами негативно влияет на общую производительность бота. Попробуйте позже.",
                    error=error,
                )
            )
        raise error

    @hybrid_group(
        name="freegames",
        description="Использует данный канал для рассылки бесплатных игр `b/freegames delete` для удаления канала",
        aliases=["free", "freeGames"],
        invoke_without_command=True,
    )
    @guild_only()
    @cooldown(rate=2, per=600, type=BucketType.guild)
    @has_permissions(administrator=True)
    @bot_has_permissions(send_messages=True)
    async def initFreeGames(self, ctx: Context):
        await ctx.message.delete()

        channel = await self.free_games_repo.get_channel_by_guild(ctx.message.guild.id)
        if channel:
            guild_channel = self.bot.get_channel(channel)
            await ctx.send(
                f"На этом сервере уже указан канал для бесплатных игр {guild_channel.mention}(удаление через 3с)", delete_after=3
            )
            return

        await self.free_games_repo.insert_channel(ctx.message.guild.id, ctx.message.channel.id)
        await ctx.send(
            "Этот канал будет использоваться для рассылки бесплатных игр (удаление через 3с)", delete_after=3
        )


    @initFreeGames.command(name="delete", description="Удаляет рассылку бесплатных игр")
    @cooldown(rate=2, per=600, type=BucketType.guild)
    @has_permissions(administrator=True)
    @bot_has_permissions(send_messages=True)
    @guild_only()
    async def removeFromFreeGames(self, ctx: Context):
        await ctx.message.delete()

        channel = await self.free_games_repo.get_channel_by_guild(ctx.message.guild.id)
        if not channel:
            await ctx.send(
                    "На этом сервере не был указан канал для бесплатных игр (удаление через 3с)", delete_after=3
                )
            return

        await self.free_games_repo.delete_channel(ctx.message.guild.id)

        await ctx.send("Рассылки игр больше не будет (удаление через 3с)")

    async def getMessages(self):
        msgs = []
        games = await self.free_games_api.get_free_games()

        for game in games:
            embedd = Embed(
                title="**Бесплатная игра недели (Epic Games)**", colour=Colour.random()
            )
            embedd.set_image(
                url=game.game_photo_url
            )
            embedd.add_field(name=f"**{game.name}**", value=f"**{game.link_to_game}**", inline=False)
            embedd.add_field(name="**Цена до раздачи: **", value=f"{game.price_before}")
            embedd.add_field(name="**Действует до: **", value=f"{game.due_date}")

            msgs.append(embedd)
        return msgs

    @hybrid_command(
        name="run_free_games",
        description="Ручной запуск бесплатных игр (только для создателей)",
    )
    @guilds(MAIN_GUILD)
    @is_owner()
    async def runFreeGanes(self, ctx: Context):
        await self.freeGames()

    async def freeGames(self):
        channels = await self.free_games_repo.get_channels()
        if len(channels) < 1:
            return

        msgs = await self.getMessages()

        for channel in channels:
            channel = self.bot.get_channel(channel)
            if not channel:
                continue

            for msg in msgs:
                announcement = await channel.send(embed=msg)

                if channel.type == ChannelType.news:
                    await announcement.publish()

                await sleep(1)


async def setup(bot):
    await bot.add_cog(FreeGames(bot))
