from discord.ext.commands import Cog
from database import db


class memberJoinRemove(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_member_join(self, member):

        insertQuery = 'with res as (insert into user_server (userid, serverid) values ($1, $2) returning id)\
                        insert into xpinfo (id) select res.id from res;'

        await self.bot.pool.execute(insertQuery, member.id, member.guild.id)

    @Cog.listener()
    async def on_member_remove(self, member):
        insertQuery = 'with res as (insert into user_server (userid, serverid) values ($1, $2) returning id)\
                        delete from user_server WHERE id = (select res.id from res);'

        await self.bot.pool.execute(insertQuery, member.id, member.guild.id)


def setup(bot):
    bot.add_cog(memberJoinRemove(bot))
