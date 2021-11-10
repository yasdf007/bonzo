from discord.channel import DMChannel
from discord.ext.commands import Cog, command, CommandOnCooldown, cooldown, BucketType, guild_only
from discord.ext.commands.context import Context
from discord import Embed, File, Asset
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from config import guilds
from discord_slash import SlashContext, cog_ext
from discord.ext import tasks
import database.db
from colorama import Fore, Back, Style


class AddXP(Cog):
    messageXP = 1
    voiceXP = 10

    def __init__(self, bot):
        self.bot = bot
        self.db_conn.start()

    @tasks.loop(count=1)
    async def db_conn(self):
        try:
            self.bot.pool = await database.db.connectToDB()
        except Exception as err:
            print(f"/ \n {Fore.RED} DB PASSWORD INVALID/ DB IS NOT SPECIFIED. ERRORS RELATED TO DATABASE DISRUPTION ARE NOT HANDLED YET. {Style.RESET_ALL}")
            print(err)
            self.bot.unload_extension(f'commands.xpSystem')

    async def cog_command_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            await ctx.message.reply(error)

    async def calculateLevel(self, exp):
        return int((exp/60) ** 0.5)

    async def calculateXp(self, lvl):
        return int(60*lvl**2)

    async def percentsToLvlUp(self, currentXp, currentLVL):
        xpToGetCurrentLVL = await self.calculateXp(currentLVL)
        xpToGetNextLVL = await self.calculateXp(currentLVL+1)

        devinded = currentXp - xpToGetCurrentLVL
        devider = xpToGetNextLVL - xpToGetCurrentLVL

        return round((devinded/devider)*100, 2)

    async def executeQuery(self, query: str, type_: str):
        async with self.bot.pool.acquire() as con:
            if type_ == 'fetch':
                result = await con.fetch(query)

            if type_ == 'fetchrow':
                result = await con.fetchrow(query)

            if type_ == 'execute':
                result = await con.execute(query)

        return result

    @Cog.listener()
    async def on_message(self, message):
        if isinstance(message.channel, DMChannel):
            return
        if message.author.bot:
            return

        await self.addMessageXp(message.author)

    async def checkAfter(self, channel):
        # Массив из людей в войсе без ботов
        membersInVoice = list(
            filter(lambda x: x.bot == False, channel.members)
        )

        # Если больше одного, то для каждого генерим опыт,
        # если уже нет таска для опыта
        if len(membersInVoice) >= 2:

            for member in membersInVoice:
                if self.bot.scheduler.get_job(f'{member.id}') is None:
                    await self.addVoiceJob(member)

    async def checkBefore(self, channel):
        membersInVoice = list(
            filter(lambda x: x.bot == False, channel.members)
        )

        if len(membersInVoice) == 1:
            for member in membersInVoice:
                self.bot.scheduler.remove_job(f'{member.id}')

    async def checkBeforeAndAfter(self, before, after):
        await self.checkBefore(before)
        await self.checkAfter(after)

    async def checkAfkOrDeaf(self, member):
        job = self.bot.scheduler.get_job(f'{member.id}')

        if job:
            if (member.voice.channel.name == member.guild.afk_channel) or member.voice.self_deaf == True:
                self.bot.scheduler.pause_job(f'{member.id}')
            else:
                self.bot.scheduler.resume_job(f'{member.id}')

    @Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.bot:
            return

        # Заход
        if after.channel and not before.channel:
            await self.checkAfter(after.channel)

        # Выход
        if before.channel and not after.channel:
            if self.bot.scheduler.get_job(f'{member.id}'):
                self.bot.scheduler.remove_job(f'{member.id}')

            await self.checkBefore(before.channel)

        # Перемещение по каналам
        if before.channel and after.channel:
            if before.channel != after.channel:
                if self.bot.scheduler.get_job(f'{member.id}'):
                    self.bot.scheduler.remove_job(f'{member.id}')

                await self.checkBeforeAndAfter(before.channel, after.channel)

        await self.checkAfkOrDeaf(member)

    async def addVoiceJob(self, member):
        self.bot.scheduler.add_job(
            self.addVoiceXp, 'interval', minutes=1, id=f'{member.id}', args=[member])

    async def addMessageXp(self, member):
        selectQuery = f'with res as (select id from user_server where userid=({member.id}) and serverid=({member.guild.id})) \
                    select xp,nexttextxpat from xpinfo where xpinfo.id = (select res.id from res);'

        xpInfo = await self.executeQuery(selectQuery, 'fetchrow')

        if xpInfo is None:
            insertQuery = f'with res as (insert into user_server (userid, serverid) values ({member.id}, {member.guild.id}) returning id) \
                        insert into xpinfo (id) select res.id from res;'
            await self.executeQuery(insertQuery, 'execute')
            return

        xp = xpInfo['xp']
        nextMessageXpAt = xpInfo['nexttextxpat']

        if datetime.now() > nextMessageXpAt:
            newXp = xp + self.messageXP
            newLvl = await self.calculateLevel(newXp)
            nextXpAt = datetime.now()+timedelta(seconds=60)

            updateQuery = f"with res as (select id from user_server where userid=({member.id}) and serverid=({member.guild.id})) \
                            update xpinfo set xp={newXp}, LVL={newLvl}, NextTextXpAt = '{nextXpAt}' \
                            where xpinfo.id = (select res.id from res);"

            await self.executeQuery(updateQuery, 'execute')

    async def addVoiceXp(self, member):
        selectQuery = f'with res as (select id from user_server where userid=({member.id}) and serverid=({member.guild.id})) \
                    select xp from xpinfo where xpinfo.id = (select res.id from res);'

        xpInfo = await self.executeQuery(selectQuery, 'fetchrow')

        if xpInfo is None:
            insertQuery = f'with res as (insert into user_server (userid, serverid) values ({member.id}, {member.guild.id}) returning id)\
                        insert into xpinfo (id) select res.id from res;'
            await self.executeQuery(insertQuery, 'execute')
            return

        newXp = xpInfo['xp'] + self.voiceXP
        newLvl = await self.calculateLevel(newXp)

        updateQuery = f'with res as (select id from user_server where userid=({member.id}) and serverid=({member.guild.id})) \
                        update xpinfo set xp={newXp}, LVL={newLvl}  where xpinfo.id = (select res.id from res);'

        await self.executeQuery(updateQuery, 'execute')

    @guild_only()
    @command(name='top', description='Показывает топ 10 по опыту')
    async def leaderboard_prefix(self, ctx: Context):
        await self.leaderboard(ctx)

    @cog_ext.cog_slash(name='top', description='Показывает топ 10 по опыту')
    async def leaderboard_slash(self, ctx: SlashContext):
        await self.leaderboard(ctx)

    async def leaderboard(self, ctx):
        selectQuery = f'select userId, xp, lvl from user_server join xpinfo ON user_server.id = xpinfo.id \
        where user_server.serverid = {ctx.guild.id} and xp > 0 order by xp desc limit 10;'

        result = await self.executeQuery(selectQuery, 'fetch')

        if result is None:
            await ctx.message.reply('Значения не найдены')
            return

        embed = Embed(
            title='TOP 10 участников по опыту', color=ctx.author.color)

        embed.set_footer(
            text=f'/by bonzo/ for {ctx.author}', icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url=ctx.guild.icon_url)

        guild = self.bot.get_guild(ctx.guild.id)

        for id_, exp, lvl in result:
            member = guild.get_member(id_)
            embed.add_field(
                name=f'`{member.display_name}`', value=f'LVL: {lvl}\nEXP: {exp}', inline=False)

        await ctx.send(embed=embed)

    @guild_only()
    @command(name='rank', description='Показывает топ 10 по опыту')
    async def rank_prefix(self, ctx: Context):
        await self.rank(ctx)

    @cog_ext.cog_slash(name='rank', description='Показывает топ 10 по опыту')
    async def rank_slash(self, ctx: SlashContext):
        await self.rank(ctx)

    async def rank(self, ctx):
        selectQuery = f'select xp,lvl,rank, overall from (select userid,xp, lvl, rank() over(order by xp desc)  from user_server \
                        join xpinfo ON user_server.id = xpinfo.id where user_server.serverid = {ctx.guild.id}) x \
                        join (select count(distinct id) as overall from user_server where serverid={ctx.guild.id}) as p on x.userid={ctx.author.id};'
        try:
            xpInfo = await self.executeQuery(selectQuery, 'fetchrow')

            xp = xpInfo['xp']
            lvl = xpInfo['lvl']
            rank = xpInfo['rank']
            maxRank = xpInfo['overall']

        except TypeError:
            await ctx.message.reply('Тебя нет в базе данных, добавляю...')
            insertQuery = f'with res as (insert into user_server (userid, serverid) values ({ctx.author.id}, {ctx.guild.id}) returning id)\
                        insert into xpinfo (id) select res.id from res;'

            await self.executeQuery(insertQuery, 'execute')

        await (await self.bot.loop.run_in_executor(None, self.asyncRankCard, ctx, xp, lvl, rank, maxRank))

    async def createMask(self, photo):
        with Image.new('L', photo.size, 0) as mask:
            drawMask = ImageDraw.Draw(mask)
            drawMask.ellipse(
                (0, 0) + photo.size, fill=255)

            return mask

    async def asyncRankCard(self, ctx, xp, lvl, rank, maxRank):
        fullBlack = (0, 0, 0)
        reqImage = await Asset.read(ctx.author.avatar_url_as(static_format='png'))

        with Image.open(BytesIO(reqImage)) as userProfilePhoto:
            with Image.open('./static/rankTemplate.png') as template:
                with Image.open('./static/progressBar.png') as bar:
                    draw = ImageDraw.Draw(template)
                    font = ImageFont.truetype('./static/arial.ttf', 14)

                    mask = await self.createMask(userProfilePhoto)

                    avatarSize = (100, 100)

                    rezised = userProfilePhoto.resize(avatarSize)
                    mask = mask.resize(avatarSize)

                    percents = await self.percentsToLvlUp(xp, lvl)
                    xpToNextLVL = await self.calculateXp(lvl+1)

                    barWidth = bar.size[0]
                    croppedBar = bar.crop((0, 0, barWidth*(percents)/100, 45))

                    template.paste(rezised, (15, 15), mask)
                    template.paste(croppedBar, (100, 255), croppedBar)

                    percentsText = f'{percents}%'
                    textWidth = font.getsize(percentsText)[0]

                    draw.text(((650-textWidth)/2, 270), percentsText, fullBlack,
                              font=font, align='right')

                    draw.text((130, 12), f'{ctx.author}', fullBlack,
                              font=font, align='center')

                    draw.text((130, 43), f'RANK:{rank}/{maxRank}', fullBlack,
                              font=font, align='center')

                    draw.text((130, 73), f'EXP: {xp}/{xpToNextLVL}', fullBlack,
                              font=font, align='center')

                    draw.text((130, 102), f'LVL: {lvl}', fullBlack,
                              font=font, align='center')

                    with BytesIO() as temp:
                        template.save(temp, 'png')
                        temp.seek(0)
                        await ctx.send(file=File(fp=temp, filename='now.png'))


def setup(bot):
    bot.add_cog(AddXP(bot))
