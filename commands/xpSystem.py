from apscheduler.jobstores.base import JobLookupError, ConflictingIdError
from discord.ext.commands import Cog, command
from database import db
from random import randint
from discord import Member, Embed
from datetime import datetime, timedelta


class AddXP(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cursor = db.cursor
        self.messageXP = 1
        self.voiceXP = 10

    @Cog.listener()
    async def on_ready(self):
        guild = self.bot.get_guild(664485208745050112)

        for channel in guild.voice_channels:
            if channel.name != 'AFK':
                for voiceUser in self.bot.get_channel(channel.id).members:
                    if not voiceUser.bot:
                        self.addVoiceJob(voiceUser)

    @Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            await self.addMessageXp(message.author.id)
        return

    @Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if not member.bot:
            print(member.voice)

            if member.voice and member.voice.channel.name != 'AFK' and member.voice.self_deaf == False:
                try:
                    self.addVoiceJob(member)
                    print(self.bot.scheduler.get_jobs())
                except ConflictingIdError:
                    pass
            else:
                print(self.bot.scheduler.get_jobs())
                try:
                    self.bot.scheduler.remove_job(f'{member.id}')
                    print(self.bot.scheduler.get_jobs())
                except JobLookupError:
                    pass

        return

    def addVoiceJob(self, member: int):
        self.bot.scheduler.add_job(
            self.addVoiceXp, 'interval', minutes=1, id=f'{member.id}', args=[member.id])

    async def addMessageXp(self, memberId: int):
        self.cursor.execute(
            'SELECT NextTextXpAt FROM exp WHERE UserId = %s', (memberId,))

        nextXpAdd = self.cursor.fetchone()[0]

        if datetime.utcnow() > nextXpAdd:
            self.cursor.execute(
                'UPDATE exp set XP = XP + %s, NextTextXpAt = %s where UserID = %s', (self.messageXP, datetime.utcnow()+timedelta(seconds=60), memberId))

        return

    async def addVoiceXp(self, memberId: int):
        self.cursor.execute(
            'UPDATE exp set XP = XP + %s where UserID = %s', (self.voiceXP, memberId))

        return

    @ command(name='leaderboard', description='Показывает топ 10 по опыту', aliases=['top'])
    async def leaderboard(self, ctx):

        self.cursor.execute(
            'SELECT UserID, XP from exp where (XP > 0) order by xp desc')
        result = self.cursor.fetchmany(10)

        if result is None:
            await ctx.send('Значения не найдены')

        embed = Embed(
            title='TOP 10 участников по опыту', color=ctx.author.color)

        embed.set_footer(
            text=f'/by bonzo/ for {ctx.message.author}', icon_url=ctx.message.author.avatar_url)
        embed.set_thumbnail(url=ctx.guild.icon_url)

        for id_, exp in result:
            member = self.bot.guild.get_member(id_)
            embed.add_field(
                name=f'`{member.display_name}`', value=f'EXP: {exp}', inline=False)
        await ctx.send(embed=embed)

        return


def setup(bot):
    bot.add_cog(AddXP(bot))
