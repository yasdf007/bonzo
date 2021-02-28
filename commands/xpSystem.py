from apscheduler.jobstores.base import JobLookupError, ConflictingIdError
from discord.ext.commands import Cog, command, CommandOnCooldown, cooldown, BucketType
from database import db
from discord import Embed, File, Asset
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO


class AddXP(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.messageXP = 1
        self.voiceXP = 10
        self.guild = None

    async def cog_command_error(self, ctx, error):
        if isinstance(error, CommandOnCooldown):
            await ctx.message.reply(error)

    @Cog.listener()
    async def on_ready(self):
        self.guild = self.bot.get_guild(664485208745050112)

        for channel in self.guild.voice_channels:
            if channel.name != 'AFK':
                for voiceUser in self.bot.get_channel(channel.id).members:
                    if not voiceUser.bot:
                        self.addVoiceJob(voiceUser)

    @Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            await self.addMessageXp(message.author)
        return

    @Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if not member.bot and member.guild.id == self.guild.id:
            # Если чел зашел в войс и не в канале АФК, и не замучен
            if member.voice and member.voice.channel.name != 'AFK' and member.voice.self_deaf == False:
                try:
                    # Добавляем таск получения опыта
                    self.addVoiceJob(member)
                # Если уже есть задача, то пофиг (если чел перемещается по каналам, то появляется ошибка,
                # поэтому дропаем в блок исключения )
                except ConflictingIdError:
                    pass

            else:
                try:
                    # Удаляем задачу
                    self.bot.scheduler.remove_job(f'{member.id}')

                # Если задачи нет, то пофиг (чел может быть в афк, т.е у него не будет задачи,
                # если он выйдет из канала афк, то появится ошибка.
                # Если зайдет в другой канал, все должно быть норм)
                except JobLookupError:
                    pass

        return

    def addVoiceJob(self, memberId: int):
        self.bot.scheduler.add_job(
            self.addVoiceXp, 'interval', minutes=1, id=f'{memberId}', args=[memberId])

    async def addMessageXp(self, member):
        selectQuery = 'with res as (select id from user_server where userid=($1) and serverid=($2)) \
                    select xp, nexttextxpat  from xpinfo where xpinfo.id = (select res.id from res);'
        async with self.bot.pool.acquire() as con:
            xpInfo = await con.fetchrow(selectQuery, member.id, member.guild.id)

            if xpInfo is None:
                insertQuery = 'with res as (insert into user_server (userid, serverid) values ($1, $2) returning id)\
                            insert into xpinfo (id) select res.id from res;'

                await con.execute(insertQuery, member.id, member.guild.id)
                return

            xp = xpInfo['xp']
            nextMessageXpAt = xpInfo['nexttextxpat']

            if datetime.now() > nextMessageXpAt:
                newXp = xp + self.messageXP
                newLvl = self.calculateLevel(newXp)

                updateQuery = 'with res as (select id from user_server where userid=($1) and serverid=($2)) \
                            update xpinfo set xp=$3, LVL=$4, NextTextXpAt = $5 where xpinfo.id = (select res.id from res);'

                await con.execute(updateQuery, member.id, member.guild.id, newXp, newLvl,
                                  datetime.now()+timedelta(seconds=60))
            await con.close()

    async def addVoiceXp(self, member):
        selectQuery = 'with res as (select id from user_server where userid=($1) and serverid=($2)) \
                    select xp from xpinfo where xpinfo.id = (select res.id from res);'
        async with self.bot.pool.acquire() as con:
            xpInfo = await con.fetchrow(selectQuery, member.id, member.guild.id)

            if xpInfo is None:
                insertQuery = 'with res as (insert into user_server (userid, serverid) values ($1, $2) returning id)\
                            insert into xpinfo (id) select res.id from res;'

                await con.execute(insertQuery, member.id, member.guild.id)
                return

            newXp = xpInfo['xp'] + self.voiceXP
            newLvl = self.calculateLevel(newXp)

            updateQuery = 'with res as (select id from user_server where userid=($1) and serverid=($2)) \
                            update xpinfo set xp=$3, LVL=$4  where xpinfo.id = (select res.id from res);'

            await con.execute(updateQuery, member.id,
                              member.guild.id, newXp, newLvl)
            await con.close()

    def calculateLevel(self, exp):
        return int((exp/45) ** 0.6)

    def calculateXp(self, lvl):
        return int((45*lvl**(5/3)))+1

    def percentsToLvlUp(self, currentXp, currentLVL):
        devinded = currentXp-self.calculateXp(currentLVL)
        devider = self.calculateXp(currentLVL+1)-self.calculateXp(currentLVL)
        return round(devinded/devider, 4)

    @command(name='leaderboard', description='Показывает топ 10 по опыту', aliases=['top'])
    async def leaderboard(self, ctx):
        selectQuery = 'select userId, xp, lvl from user_server join xpinfo ON user_server.id = xpinfo.id where user_server.serverid = $1 and xp > 0 order by xp desc;'
        async with self.bot.pool.acquire() as con:
            result = await con.fetch(selectQuery, ctx.guild.id)
            await con.close()
        if result is None:
            await ctx.message.reply('Значения не найдены')
            return

        embed = Embed(
            title='TOP 10 участников по опыту', color=ctx.author.color)

        embed.set_footer(
            text=f'/by bonzo/ for {ctx.message.author}', icon_url=ctx.message.author.avatar_url)
        embed.set_thumbnail(url=ctx.guild.icon_url)

        for id_, exp, lvl in result:
            member = self.bot.guild.get_member(id_)
            embed.add_field(
                name=f'`{member.display_name}`', value=f'LVL: {lvl}\nEXP: {exp}', inline=False)
        await ctx.message.reply(embed=embed)

    @cooldown(rate=1, per=60, type=BucketType.user)
    @command(name='rank', description='Показывает карточку с опытом')
    async def rank(self, ctx):
        selectQuery = 'with res as (select id from user_server where userid=($1) and serverid=($2)) \
                    select xp, lvl from xpinfo where xpinfo.id = (select res.id from res);'
        async with self.bot.pool.acquire() as con:
            try:
                xp, lvl = await con.fetchrow(
                    selectQuery, ctx.author.id, ctx.guild.id)
            except TypeError:
                await ctx.message.reply('Тебя нет в базе данных, добавляю...')
                insertQuery = 'with res as (insert into user_server (userid, serverid) values ($1, $2) returning id)\
                            insert into xpinfo (id) select res.id from res;'

                await con.execute(insertQuery, ctx.author.id, ctx.guild.id)
                return
            await con.close()

        reqImage = await Asset.read(ctx.author.avatar_url)

        userProfilePhoto = Image.open(BytesIO(reqImage))
        template = Image.open('./static/rankTemplate.png')
        bar = Image.open('./static/progressBar.png')

        draw = ImageDraw.Draw(template)
        font = ImageFont.truetype('./static/arial.ttf', 14)

        rezised = userProfilePhoto.resize((100, 100))
        w, _ = bar.size

        percents = self.percentsToLvlUp(xp, lvl)

        cropped = bar.crop((0, 0, w*percents, 45))

        template.paste(rezised, (15, 15))
        template.paste(cropped, (100, 255), cropped)

        draw.text((300, 270), f'{percents*100}%', (0, 0, 0),
                  font=font, align='center')
        draw.text((130, 12), f'{ctx.author.name}#{ctx.author.discriminator}', (0, 0, 0),
                  font=font, align='center')
        draw.text((130, 43), 'NO RANK FUNCTIONALITY IMPLEMENTED', (0, 0, 0),
                  font=font, align='center')
        draw.text((130, 73), f'EXP: {xp}', (0, 0, 0),
                  font=font, align='center')
        draw.text((130, 102), f'LVL: {lvl}', (0, 0, 0),
                  font=font, align='center')

        with BytesIO() as temp:
            template.save(temp, "png", quality=100)
            temp.seek(0)
            await ctx.message.reply(file=File(fp=temp, filename='now.jpeg'))


def setup(bot):
    bot.add_cog(AddXP(bot))
