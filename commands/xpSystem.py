from asyncio.tasks import sleep
from discord.ext.commands import Cog
from dbLite import db
from random import randint
from discord import Member
from asyncio import create_task, sleep


class AddXP(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cursor = db.cursor
        self.textChannel = self.bot.get_channel(681179689775398943)
        self.voiceChannel = self.bot.get_channel(700677946607927356)
        self.tasksDict = {}

    @Cog.listener()
    async def on_message(self, message):
        if not message.author.bot and message.channel == self.textChannel:
            self.addXp(message.author)
        return

    @Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if not member.bot:

            if not before.channel:
                task = create_task(self.voiceTask(member))
                self.tasksDict.update({member.id: task})
            if before.channel and not after.channel:
                for key, value in self.tasksDict.items():
                    if member.id == key:
                        value.cancel()
                del self.tasksDict[member.id]
        return

    def addXp(self, member: Member):
        cursor = self.cursor

        cursor.execute(f'SELECT XP from exp where UserID = {member.id}', )
        result = cursor.fetchone()
        if result is None:
            cursor.execute(
                'INSERT INTO exp VALUES (?, ?, ?)', (member.name, member.id, 0))
        else:
            cursor.execute(
                f'UPDATE exp set XP = XP + {randint(1, 15)} where UserID = {member.id}')

    def addVoiceXp(self, member: Member):
        cursor = self.cursor

        cursor.execute(f'SELECT XP from exp where UserID = {member.id}', )
        result = cursor.fetchone()
        if result is None:
            cursor.execute(
                'INSERT INTO exp VALUES (?, ?, ?)', (member.name, member.id, 0))
        else:
            cursor.execute(
                f'UPDATE exp set XP = XP + {randint(50, 100)} where UserID = {member.id}')
        pass

    async def voiceTask(self, member):
        while True:
            self.addVoiceXp(member)
            await sleep(3)


def setup(bot):
    bot.add_cog(AddXP(bot))
