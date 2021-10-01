from os import name
from discord.ext.commands import Cog, guild_only, has_permissions, bot_has_permissions, group, BucketType, cooldown
from aiohttp import ClientSession
from apscheduler.triggers.cron import CronTrigger
from asyncio import sleep
from discord.ext.commands import command
from discord.ext.commands.errors import CommandOnCooldown, MissingPermissions, NoPrivateMessage
from datetime import datetime
from discord.enums import ChannelType
from discord import Embed
from .resources.animationFW import randCol


class FreeGames(Cog):
    link = 'https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions?locale=ru&country=RU&allowCountries=RU'

    def __init__(self, bot):
        self.bot = bot
        self.bot.scheduler.add_job(
            self.freeGames, CronTrigger(day_of_week='thu', hour=19, minute=3, jitter=120))

    async def cog_command_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.message.reply('Только администратор может использовать эту команду')
        if isinstance(error, NoPrivateMessage):
            await ctx.send('Только на серверах')
        if isinstance(error, CommandOnCooldown):
            await ctx.message.reply(f'Server cooldown. Try again in {error.retry_after:.2f}s')

    @guild_only()
    @cooldown(rate=2, per=600, type=BucketType.guild)
    @has_permissions(administrator=True)
    @bot_has_permissions(send_messages=True)
    @group(name='freegames', description='Использует данный канал для рассылки бесплатных игр `b/freegames delete` для удаления канала', aliases=['free', 'freeGames'], invoke_without_command=True)
    async def initFreeGames(self, ctx):
        await ctx.message.delete()

        try:
            async with self.bot.pool.acquire() as con:
                selectQuery = f'select channel_id from free_games_channel where server_id={ctx.message.guild.id}'
                res = await con.fetchrow(selectQuery)
                if res:
                    channel = self.bot.get_channel(res['channel_id'])
                    msg = await ctx.send(f'На этом сервере уже указан канал для бесплатных игр {channel.mention}(удаление через 3с)')
                    await sleep(3)
                    await msg.delete()
                    return

                insertQuery = f'insert into free_games_channel(server_id,channel_id) values({ctx.message.guild.id},{ctx.message.channel.id});'
                await con.execute(insertQuery)

                msg = await ctx.send('Этот канал будет использоваться для рассылки бесплатных игр (удаление через 3с)')
                await sleep(3)
        except:
            msg = await ctx.send('Ошибка при инициализации канала (удаление через 3с)')
            await sleep(3)

        await msg.delete()

    @guild_only()
    @cooldown(rate=2, per=600, type=BucketType.guild)
    @has_permissions(administrator=True)
    @initFreeGames.command(name='delete', description='Удаляет рассылку бесплатных игр')
    @bot_has_permissions(send_messages=True)
    async def removeFromFreeGames(self, ctx):
        await ctx.message.delete()
        async with self.bot.pool.acquire() as con:
            selectQuery = f'select channel_id from free_games_channel where server_id={ctx.message.guild.id}'
            res = await con.fetchrow(selectQuery)

            if not res:
                msg = await ctx.send('На этом сервере не был указан канал для бесплатных игр (удаление через 3с)')
                await sleep(3)
                await msg.delete()
                return

            deleteQuery = f'delete from free_games_channel where server_id={ctx.message.guild.id}'
            await con.execute(deleteQuery)

            msg = await ctx.send('Рассылки игр больше не будет (удаление через 3с)')
            await sleep(3)
            await msg.delete()

    async def getChannels(self):
        selectQuery = f'select channel_id from free_games_channel'
        async with self.bot.pool.acquire() as con:
            res = await con.fetch(selectQuery)

        return res

    async def getMessages(self):
        async with ClientSession() as session:
            async with session.get(self.link) as response:
                resultJson = await response.json()

        games = resultJson['data']['Catalog']['searchStore']['elements']
        msgs = []
        for game in games:
            promotions = game['promotions']

            if promotions == None:
                continue

            freeDiscountSetting = promotions['promotionalOffers'][0][
                'promotionalOffers'][0]['discountSetting']['discountPercentage']

            if freeDiscountSetting != 0:
                continue

            due_date = datetime.fromisoformat(promotions['promotionalOffers'][0][
                'promotionalOffers'][0]['endDate'][:-1]).strftime('%d/%m/%Y')

            game_name = game['title']

            slug = game['productSlug']

            link = 'https://www.epicgames.com/store/ru/p/' + slug

            embedd = Embed(
                title='**Бесплатная игра недели (Epic Games)**', colour=await randCol())
            embedd.set_thumbnail(
                url='https://www.dsogaming.com/wp-content/uploads/2020/04/epicgames.jpg')
            embedd.add_field(
                name=f'**{game_name}**', value=f'**{link}**'
            )
            embedd.add_field(
                name='**Действует до: **', value=f'{due_date}'
            )

            msgs.append(embedd)
        return msgs

    async def freeGames(self):
        channels = await self.getChannels()
        if len(channels) < 1:
            return
        msgs = await self.getMessages()

        for channel in channels:
            channel = self.bot.get_channel(channel['channel_id'])
            for msg in msgs:
                announcement = await channel.send(embed=msg)

                if channel.type == ChannelType.news:
                    await announcement.publish()

                await sleep(1)


def setup(bot):
    bot.add_cog(FreeGames(bot))
