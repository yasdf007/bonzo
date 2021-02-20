from apscheduler.jobstores.base import JobLookupError
from discord.ext.commands import Cog, command
from database import db
from random import randint
from discord import Member, Embed


class AddXP(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cursor = db.cursor

    @Cog.listener()
    async def on_ready(self):
        guild = self.bot.get_guild(664485208745050112)

        for channel in guild.voice_channels:
            if channel.name != 'AFK':
                for voiceUser in self.bot.get_channel(channel.id).members:
                    if not voiceUser.bot:
                        self.bot.scheduler.add_job(
                            self.addVoiceXp, 'interval', seconds=30, id=f'{voiceUser.id}', args=[voiceUser])

    @Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            await self.addXp(message.author)
        return

    @Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if not member.bot:

            if not before.channel or (before.channel.name == 'AFK' and after.channel is not None):
                self.bot.scheduler.add_job(
                    self.addVoiceXp, 'interval', seconds=30, id=f'{member.id}', args=[member])

            elif (before.channel and (not after.channel or after.channel.name == 'AFK')):
                try:
                    self.bot.scheduler.remove_job(f'{member.id}')
                except JobLookupError:
                    pass

        return

    async def addXp(self, member: Member):

        self.cursor.execute(f'SELECT XP from exp where UserID = {member.id}', )
        self.cursor.fetchone()
        self.cursor.execute(
            f'UPDATE exp set XP = XP + {randint(1, 2)} where UserID = {member.id}')

        return

    async def addVoiceXp(self, member: Member):

        self.cursor.execute(f'SELECT XP from exp where UserID = {member.id}', )
        self.cursor.fetchone()
        self.cursor.execute(
            f'UPDATE exp set XP = XP + {randint(15, 25)} where UserID = {member.id}')

        return

    @command(name='leaderboard', description='Показывает топ 10 по опыту', aliases=['top'])
    async def leaderboard(self, ctx):

        self.cursor.execute(
            'SELECT username, XP from exp where (XP > 0) order by xp desc')
        result = self.cursor.fetchmany(10)

        if result is None:
            await ctx.send('Значения не найдены')

        embed = Embed(
            title=f'Топ 10 по опыту {ctx.guild.name}', color=ctx.author.color)
        embed.set_footer(
            text=f'/by bonzo/ for {ctx.message.author}', icon_url=ctx.message.author.avatar_url)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        for name, exp in result:
            embed.add_field(name=f'`{name}`', value=exp, inline=False)
        await ctx.send(embed=embed)

        return


def setup(bot):
    bot.add_cog(AddXP(bot))
