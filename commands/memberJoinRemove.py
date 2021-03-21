from discord.ext.commands import Cog


class memberJoinRemove(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_member_join(self, member):

        insertQuery = f'with res as (insert into user_server (userid, serverid) values ({member.id}, {member.guild.id}) returning id)\
                        insert into xpinfo (id) select res.id from res;'

        await self.bot.pool.execute(insertQuery)

    @Cog.listener()
    async def on_member_remove(self, member):
        deleteQuery = f'delete from user_server WHERE userid = {member.id} and serverid = {member.guild.id};'

        await self.bot.pool.execute(deleteQuery)


def setup(bot):
    bot.add_cog(memberJoinRemove(bot))
