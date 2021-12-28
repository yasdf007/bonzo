from os import name
from discord.ext.commands import (
    Cog,
    guild_only,
    has_permissions,
    bot_has_permissions,
    group,
    BucketType,
    cooldown,
)
from aiohttp import ClientSession
from apscheduler.triggers.cron import CronTrigger
from asyncio import sleep
from discord.ext.commands import command
from discord.ext.commands.core import is_owner
from discord.ext.commands.errors import (
    CommandInvokeError,
    CommandOnCooldown,
    MissingPermissions,
    NoPrivateMessage,
)
from datetime import datetime
from discord.enums import ChannelType
from discord import Embed
from discord import Colour
from .resources.AutomatedMessages import automata


class FreeGames(Cog):
    link = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions?locale=ru&country=RU&allowCountries=RU"

    def __init__(self, bot):
        self.bot = bot
        self.bot.scheduler.add_job(
            self.freeGames,
            CronTrigger(day_of_week="thu", hour=19, minute=3, jitter=120),
        )

    async def cog_command_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.message.reply(
                embed=automata.generateEmbErr(
                    "Только администратор может использовать эту команду", error=error
                )
            )
        if isinstance(error, NoPrivateMessage):
            await ctx.send(
                embed=automata.generateEmbErr("Только на серверах", error=error)
            )
        if isinstance(error, CommandOnCooldown):
            await ctx.message.reply(
                embed=automata.generateEmbErr(
                    "Спам командами негативно влияет на общую производительность бота. Попробуйте позже.",
                    error=error,
                )
            )
        raise error

    @guild_only()
    @cooldown(rate=2, per=600, type=BucketType.guild)
    @has_permissions(administrator=True)
    @bot_has_permissions(send_messages=True)
    @group(
        name="freegames",
        description="Использует данный канал для рассылки бесплатных игр `b/freegames delete` для удаления канала",
        aliases=["free", "freeGames"],
        invoke_without_command=True,
    )
    async def initFreeGames(self, ctx):
        await ctx.message.delete()

        try:
            async with self.bot.pool.acquire() as con:
                selectQuery = f"select free_games_channel_id from server_settings where server_id={ctx.message.guild.id}"
                res = await con.fetchrow(selectQuery)

                if res != None and res["free_games_channel_id"] != None:
                    channel = self.bot.get_channel(res["free_games_channel_id"])
                    msg = await ctx.send(
                        f"На этом сервере уже указан канал для бесплатных игр {channel.mention}(удаление через 3с)"
                    )
                    await sleep(3)
                    await msg.delete()
                    return

                insertQuery = f"""
                insert into server_settings(server_id, free_games_channel_id) values({ctx.message.guild.id},{ctx.message.channel.id})
                ON CONFLICT (server_id) DO UPDATE SET free_games_channel_id={ctx.message.channel.id};
                """
                await con.execute(insertQuery)

                msg = await ctx.send(
                    "Этот канал будет использоваться для рассылки бесплатных игр (удаление через 3с)"
                )
                await sleep(3)
        except:
            msg = await ctx.send("Ошибка при инициализации канала (удаление через 3с)")
            await sleep(3)

        await msg.delete()

    @guild_only()
    @cooldown(rate=2, per=600, type=BucketType.guild)
    @has_permissions(administrator=True)
    @initFreeGames.command(name="delete", description="Удаляет рассылку бесплатных игр")
    @bot_has_permissions(send_messages=True)
    async def removeFromFreeGames(self, ctx):
        await ctx.message.delete()
        async with self.bot.pool.acquire() as con:
            selectQuery = f"select free_games_channel_id from server_settings where server_id={ctx.message.guild.id};"
            res = await con.fetchrow(selectQuery)

            if res == None or res["free_games_channel_id"] == None:
                msg = await ctx.send(
                    "На этом сервере не был указан канал для бесплатных игр (удаление через 3с)"
                )
                await sleep(3)
                await msg.delete()
                return

            deleteQuery = f"update server_settings set free_games_channel_id = null where server_id={ctx.message.guild.id}"
            await con.execute(deleteQuery)

            msg = await ctx.send("Рассылки игр больше не будет (удаление через 3с)")
            await sleep(3)
            await msg.delete()

    async def getChannels(self):
        selectQuery = f"select free_games_channel_id from server_settings;"
        async with self.bot.pool.acquire() as con:
            res = await con.fetch(selectQuery)

        return res

    async def getMessages(self):
        async with ClientSession() as session:
            try:
                async with session.get(self.link) as response:
                    resultJson = await response.json()
            except:
                raise CommandInvokeError("Ошибка при запросе")

        games = resultJson["data"]["Catalog"]["searchStore"]["elements"]
        msgs = []

        for game in games:
            promotions = game["promotions"]

            if not promotions:
                continue

            if len(promotions["promotionalOffers"]) == 0:
                continue

            freeDiscountSetting = promotions["promotionalOffers"][0][
                "promotionalOffers"
            ][0]["discountSetting"]["discountPercentage"]

            if freeDiscountSetting != 0:
                continue

            due_date = datetime.fromisoformat(
                promotions["promotionalOffers"][0]["promotionalOffers"][0]["endDate"][
                    :-1
                ]
            ).strftime("%d/%m/%Y")

            game_name = game["title"]

            slug = game["urlSlug"]

            link = "https://www.epicgames.com/store/ru/p/" + slug

            embedd = Embed(
                title="**Бесплатная игра недели (Epic Games)**", colour=Colour.random()
            )
            embedd.set_thumbnail(
                url="https://www.dsogaming.com/wp-content/uploads/2020/04/epicgames.jpg"
            )
            embedd.add_field(name=f"**{game_name}**", value=f"**{link}**")
            embedd.add_field(name="**Действует до: **", value=f"{due_date}")

            msgs.append(embedd)
        return msgs

    @command(
        name="run_free_games",
        description="Ручной запуск бесплатных игр (только для создателей)",
    )
    @is_owner()
    async def runFreeGanes(self, ctx):
        await self.freeGames()

    async def freeGames(self):
        channels = await self.getChannels()
        if len(channels) < 1:
            return
        msgs = await self.getMessages()

        for channel in channels:
            channel = self.bot.get_channel(channel["free_games_channel_id"])
            if not channel:
                continue

            for msg in msgs:
                announcement = await channel.send(embed=msg)

                if channel.type == ChannelType.news:
                    await announcement.publish()

                await sleep(1)


def setup(bot):
    bot.add_cog(FreeGames(bot))
