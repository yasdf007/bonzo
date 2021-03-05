from apscheduler.jobstores.base import JobLookupError, ConflictingIdError
from discord.ext.commands import Cog, command, CommandOnCooldown, cooldown, BucketType
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

    def calculateLevel(self, exp):
        return int((exp/60) ** 0.5)

    def calculateXp(self, lvl):
        return int(60*lvl**2)

    def percentsToLvlUp(self, currentXp, currentLVL):
        devinded = currentXp-self.calculateXp(currentLVL)
        devider = self.calculateXp(currentLVL+1)-self.calculateXp(currentLVL)
        return round(devinded/devider, 4)

    async def executeQuery(self, query: str, type_: str):
        async with self.bot.pool.acquire() as con:
            if type_ == 'fetch':
                result = await con.fetch(query)

            if type_ == 'fetchrow':
                result = await con.fetchrow(query)

            if type_ == 'execute':
                result = await con.execute(query)

        await self.bot.pool.release(con)

        return result

    @Cog.listener()
    async def on_ready(self):
        self.guild = self.bot.get_guild(664485208745050112)

        for channel in self.guild.voice_channels:
            if channel.name != self.guild.afk_channel:
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
            if member.voice and member.voice.channel.name != self.guild.afk_channel and member.voice.self_deaf == False:
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
            newLvl = self.calculateLevel(newXp)
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
        newLvl = self.calculateLevel(newXp)

        updateQuery = f'with res as (select id from user_server where userid=({member.id}) and serverid=({member.guild.id})) \
                        update xpinfo set xp={newXp}, LVL={newLvl}  where xpinfo.id = (select res.id from res);'

        await self.executeQuery(updateQuery, 'execute')

    @cooldown(rate=1, per=20, type=BucketType.user)
    @command(name='leaderboard', description='Показывает топ 10 по опыту', aliases=['top'])
    async def leaderboard(self, ctx):
        selectQuery = f'select userId, xp, lvl from user_server join xpinfo ON user_server.id = xpinfo.id \
        where user_server.serverid = {ctx.guild.id} and xp > 0 order by xp desc;'

        result = await self.executeQuery(selectQuery, 'fetch')

        if result is None:
            await ctx.message.reply('Значения не найдены')
            return

        embed = Embed(
            title='TOP 10 участников по опыту', color=ctx.author.color)

        embed.set_footer(
            text=f'/by bonzo/ for {ctx.message.author}', icon_url=ctx.message.author.avatar_url)
        embed.set_thumbnail(url=ctx.guild.icon_url)

        guild = self.bot.get_guild(ctx.guild.id)

        for id_, exp, lvl in result:
            member = guild.get_member(id_)
            embed.add_field(
                name=f'`{member.display_name}`', value=f'LVL: {lvl}\nEXP: {exp}', inline=False)
        await ctx.message.reply(embed=embed)

    @cooldown(rate=1, per=60, type=BucketType.user)
    @command(name='rank', description='Показывает карточку с опытом')
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

        percentsText = f'{percents*100}%'
        textWidth = font.getsize(percentsText)[0]

        draw.text(((650-textWidth)/2, 270), percentsText, (0, 0, 0),
                  font=font, align='right')
        draw.text((130, 12), f'{ctx.author.name}#{ctx.author.discriminator}', (0, 0, 0),
                  font=font, align='center')
        draw.text((130, 43), f'RANK:{rank}/{maxRank}', (0, 0, 0),
                  font=font, align='center')
        draw.text((130, 73), f'EXP: {xp}', (0, 0, 0),
                  font=font, align='center')
        draw.text((130, 102), f'LVL: {lvl}', (0, 0, 0),
                  font=font, align='center')

        with BytesIO() as temp:
            template.save(temp, "png", quality=100)
            temp.seek(0)
            await ctx.message.reply(file=File(fp=temp, filename='now.jpeg'))
        temp.close()


def setup(bot):
    bot.add_cog(AddXP(bot))
