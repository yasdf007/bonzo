from discord.ext.commands import Cog
from database import db


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
        insertQuery = f'with res as (insert into user_server (userid, serverid) values ({member.id}, {member.guild.id}) returning id)\
                        delete from user_server WHERE id = (select res.id from res);'

        await self.bot.pool.execute(insertQuery)


def setup(bot):
    bot.add_cog(memberJoinRemove(bot))
