from discord.ext.commands import Cog, guild_only, has_permissions, group, bot_has_permissions
from aiohttp import ClientSession
from apscheduler.triggers.cron import CronTrigger
from asyncio import sleep


from discord.ext.commands.errors import MissingPermissions, NoPrivateMessage


class FreeGames(Cog):
    link = 'https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions?locale=ru&country=RU&allowCountries=RU'

    def __init__(self, bot):
        self.bot = bot
        self.bot.scheduler.add_job(
            self.freeGames, CronTrigger(day_of_week='thu', hour=16, minute=3, jitter=120))

    async def cog_command_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.message.reply('Только администратор может использовать эту команду')
        if isinstance(error, NoPrivateMessage):
            await ctx.send('Только на серверах')

    @guild_only()
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
                    msg = await ctx.send(f'На этом сервере уже указан канал для бесплатных игр {ctx.channel.mention}(удаление через 3с)')
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
    @initFreeGames.command(name='delete', description='Удаляет рассылку бесплатных игр')
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

    async def getUrls(self):
        async with ClientSession() as session:
            async with session.get(self.link) as response:
                resultJson = await response.json()

        games = resultJson['data']['Catalog']['searchStore']['elements']
        msgs = []
        for game in games:
            promotions = game['promotions']

            if promotions:
                gameProm = promotions['promotionalOffers']

                if gameProm:
                    game_name = game['title']

                    for attr in game['customAttributes']:
                        if attr['key'] == "com.epicgames.app.productSlug":
                            slug = attr['value']

                    link = 'https://www.epicgames.com/store/ru/p/' + slug

                    msgs.append(
                        f'Прямо сейчас бесплатна {game_name}\nСсылка {link}')
        return msgs

    async def freeGames(self):
        channels = await self.getChannels()
        if len(channels) < 1:
            return

        msgs = await self.getUrls()
        for channel in channels:
            channel = self.bot.get_channel(channel['channel_id'])

            for msg in msgs:
                await channel.send(msg)
                await sleep(1)


def setup(bot):
    bot.add_cog(FreeGames(bot))
