from discord.ext.commands import Cog
from database import db


class memberJoinRemove(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cursor = db.cursor

    @Cog.listener()
    async def on_member_join(self, member):
        db.execute(
            f"INSERT into exp (username, UserID) VALUES ({member.name}, {member.id}) ON CONFLICT (UserID) DO NOTHING;",)

    @Cog.listener()
    async def on_member_remove(self, member):
        db.execute(f'DELETE FROM exp WHERE UserID = {member.id}')


def setup(bot):
    bot.add_cog(memberJoinRemove(bot))
